from typing import Container, Callable
from loguru import logger

from dependency_injector.wiring import inject, Provide
from fastapi import Depends

from app.core.settings.app import AppSettings
from app.db.events import test_mongodb_connection
from app.api.dependencies.container import Container
from app.db.clients.mongo import MongoClient

def create_start_app_handler(settings: AppSettings) -> Callable:
    async def start_app() -> None:
        logger.debug(f"Starting {settings.title} application")
    
    return start_app


def create_stop_app_handler(settings: AppSettings) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        ...
    
    return stop_app

