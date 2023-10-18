import os
import sys

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from contextlib import asynccontextmanager

# Add the parent directory (app) to sys.path
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, parent_directory)

from app.core.config import get_app_settings
from app.core.events import (
    create_start_app_handler,
    create_stop_app_handler
)
from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.dependencies.middleware import add_process_time_header
from app.api.routes.api import router as api_router
from app.api.dependencies.container import Container
from app.api.dependencies.cache import CacheService
from app.db.clients.mongo import MongoClient
from app.db.events import test_mongodb_connection, stop_mongodb, test_cache_service
from app.core.config import get_app_settings


container_modules = [
        __name__, 
        "app.api.routes.api",
        "app.core.events",
    ]


def get_container() -> Container:
    container = Container()
    container.config.redis_settings.from_value(get_app_settings().redis)
    container.config.mongo_settings.from_value(get_app_settings().mongo)
    container.wire(modules=container_modules)
    return container


@inject
async def startup(mongo_db: MongoClient = Depends(Provide[Container.mongo_db]),
                  cache_service: CacheService = Depends(Provide[Container.cache_service])):
    await test_mongodb_connection(mongo_db)
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
    application = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(api_router, prefix=settings.api_prefix)
    
    return application


app = get_application()
container = get_container()


