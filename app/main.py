from fastapi import FastAPI, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

import logging
import os
import sys
import time

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the parent directory (app) to sys.path
current_directory =  os.path.abspath(os.path.dirname(__file__))
logger.debug(current_directory)

parent_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, parent_directory)

from app.dependencies.service_models import ServiceException, Tags
from app.dependencies.functions import isNotNull, get_settings
from app.dependencies.constants import AppSettingsDependency
from app.routers import teams
from app.dependencies.containers import Container
from app.dependencies.services import Service
from dependency_injector.wiring import inject, Provide


app_settings = get_settings()

# Application
app = FastAPI(title= "Footy Data Sync API", version="v1.0")
app.include_router(teams.router)

# Decorators
@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exec: ServiceException):
    return jsonable_encoder(JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {"service": exec.name, "message": exec.message}
    ))

# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"method={request.method}, path={request.url.path}, response_time={process_time}")
    return response    


@app.get("/", tags=[Tags.app], name="Health check")
async def health(settings: AppSettingsDependency) -> Any:
    return {"status": f"{settings.app_name} service is running."}


@app.get("/settings", tags=[Tags.app], name="App Settings")
async def settings(settings: AppSettingsDependency) -> Any:
    return {
        "mongo": isNotNull(settings.mongo),
        "redis": isNotNull(settings.redis),
        "bigquery": isNotNull(settings.bigquery),
        "rapid_api_keys": isNotNull(settings.rapid_api)
    }

@app.get("/redis/connect/test", tags=[Tags.app], name="Connection test for Redis")
@inject
async def test_dependency(service: Service = Depends(Provide[Container.service])):
    value = await service.redis_conn_test()
    return {"connection": value}


#Container
container = Container()
container.config.redis_host.from_value(app_settings.redis.hostname)
container.config.redis_port.from_value(app_settings.redis.port)
container.config.redis_password.from_value(app_settings.redis.password)
container.config.redis_max_connections.from_value(app_settings.redis.max_connections)
container.wire(modules=[__name__])