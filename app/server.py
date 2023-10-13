from fastapi import FastAPI, status, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from dependency_injector.wiring import inject, Provide

import os
import sys
import time

# Add the parent directory (app) to sys.path
current_directory =  os.path.abspath(os.path.dirname(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, ".."))
sys.path.insert(0, parent_directory)

from app.dependencies.exceptions import ServiceException
from app.dependencies.functions import get_settings
from app.dependencies.containers import Container
from app.dependencies.logger import get_logger
from app.internal.db.mongo import MongoClient
from app.routers import teams, admin

logger = get_logger(__name__)

app_settings = get_settings()

# Application
def create_app() -> FastAPI:
    app = FastAPI(title= "Footy Data Sync API", version="v1.0")
    app.include_router(admin.router)
    app.include_router(teams.router)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

# Create FastAPI app
app = create_app()

# Instrumentation
instrumentator = Instrumentator().instrument(app=app)

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


@app.on_event("startup")
@inject
async def startup(mongo_db: MongoClient = Depends(Provide[Container.mongo_db])):
    logger.info("Connecting to MongoDB")
    try:
        is_connected = await mongo_db.is_connected()
        logger.debug(is_connected)
        logger.info(
            "Connected to MongoDB -  %s environment!", os.getenv("ENVIRONMENT", "DEV")
        )
    except ConnectionError as e:
        raise Exception(e)
    
    instrumentator.expose(app)
    

@app.on_event("shutdown")
@inject
async def shutdown(mongo_db: MongoClient = Depends(Provide[Container.mongo_db])):
    logger.info("Closing connection to MongoDB")
    try:
        mongo_db.close()
        logger.info(
            logger.info("MongoDB connection closed")
        )
    except ConnectionError as e:
        raise Exception(e)
    

def mongo_uri() -> str:
    username = app_settings.mongo.username
    password = app_settings.mongo.password
    hostname = app_settings.mongo.hostname
    return f"mongodb+srv://{username}:{password}@{hostname}/?retryWrites=true&w=majority"


container = Container()
container.config.redis_settings.from_value(app_settings.redis)
container.config.mongo_uri.from_value(mongo_uri())
container.config.mongo_settings.from_value(app_settings.mongo)
container.wire(modules=[__name__, 
                        "app.routers.admin",
                        "app.routers.teams"
                        ])
    
