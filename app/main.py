from fastapi import FastAPI, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from functools import lru_cache
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
from app.dependencies.functions import isNotNull
from app.dependencies.constants import AppSettings
from app.routers import teams

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
async def health(settings: AppSettings) -> Any:
    return {"status": f"{settings.app_name} service is running."}


@app.get("/settings", tags=[Tags.app], name="App Settings")
async def settings(settings: AppSettings) -> Any:
    return {
        "mongo": isNotNull(settings.mongo),
        "redis": isNotNull(settings.redis),
        "bigquery": isNotNull(settings.bigquery),
        "rapid_api_keys": isNotNull(settings.rapid_api)
    }
