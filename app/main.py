import os
import sys
import time

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from app.api.dependencies.adapter import ContainderAdapter
from app.api.dependencies.container import Container

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

def get_container() -> Container:
    adapter = ContainderAdapter()
    container = Container()
    adapter.config.redis_settings.from_value(get_app_settings().redis)
    adapter.config.mongo_settings.from_value(get_app_settings().mongo)
    container.wire(modules=[__name__, 
                            "app.api.routes.api",
                            ])

    return container


def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()
    application = FastAPI(**settings.fastapi_kwargs)
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    application.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
    
    application.add_event_handler(
        "startup",
        create_start_app_handler(settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(settings),
    )
    
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    
    application.include_router(api_router, prefix=settings.api_prefix)

    return application


app = get_application()
container = get_container()