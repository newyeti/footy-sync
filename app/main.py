import os
import sys
import uvicorn
import logging

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager

# Add the parent directory (app) to sys.path
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, parent_directory)

from app.core.config import get_app_settings
from app.api.errors.service_error import service_error_handler, ServiceException
from app.api.errors.app_error import app_error_handler, AppException
from app.api.errors.http_error import http_error_handler
from app.api.dependencies.middleware import add_process_time_header, PrometheusMiddleware
from app.api.dependencies.container import Container
from app.api.dependencies.cache import CacheService
from app.db.clients.mongo import MongoClient
from app.db.events import test_mongodb_connection, stop_mongodb, test_cache_service, test_bigquery_connection
from app.db.clients.bigquery import BigQueryClient
from app.api.routes.api import router as api_router
from app.api.errors.validation_error import http422_error_handler
from app.api.utils import setting_otlp

APP_NAME = os.environ.get("APP_NAME", "footy-sync")
EXPOSE_PORT = int(os.environ.get("EXPOSE_PORT", 8000))
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
ROOT_CONTEXT = os.environ.get("ROOT_CONTEXT", "")

container_modules = [
        __name__, 
        "app.api.routes.teams",
        "app.api.routes.fixtures",
        "app.core.events",
    ]


def get_container() -> Container:
    container = Container()
    container.config.redis_settings.from_value(get_app_settings().infra.redis)
    container.config.mongo_settings.from_value(get_app_settings().infra.mongo)
    container.config.bigquery_settings.from_value(
        get_app_settings().infra.bigquery)
    container.config.rapid_api_settings.from_value(get_app_settings().rapid_api)
    container.wire(modules=container_modules)
    return container


@inject
async def startup(mongo_db: MongoClient = Depends(Provide[Container.mongo_db]),
                  cache_service: CacheService = Depends(
                      Provide[Container.cache_service]),
                  bigquery_client: BigQueryClient = Depends(
                      Provide[Container.bigquery])
                  ):
    await test_mongodb_connection(mongo_db)
    await test_bigquery_connection(bigquery_client)
    await test_cache_service(cache_service)


@inject
async def shutdown(mongo_db: MongoClient = Depends(Provide[Container.mongo_db])):
    await stop_mongodb(mongo_db)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    application = FastAPI(lifespan=lifespan, root_path=ROOT_CONTEXT, **settings.fastapi_kwargs) 
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.add_exception_handler(ServiceException, service_error_handler)
    application.add_exception_handler(AppException, app_error_handler)
    application.include_router(api_router, prefix=settings.api_prefix)
    
    return application


app = get_application()
container = get_container()
setting_otlp(app=app, app_name=APP_NAME, endpoint=OTLP_GRPC_ENDPOINT)

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

if __name__ == "__main__":
    # update uvicorn access logger format
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, root_path=ROOT_CONTEXT ,log_config=log_config)
