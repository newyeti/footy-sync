from typing import Callable
from loguru import logger
from app.core.settings.app import AppSettings


def create_start_app_handler(settings: AppSettings) -> Callable:
    async def start_app() -> None:
        logger.debug(f"Starting {settings.title} application")
    
    return start_app


def create_stop_app_handler(settings: AppSettings) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        logger.debug(f"Stopping {settings.title} application")
    
    return stop_app

