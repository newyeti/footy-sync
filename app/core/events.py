from typing import Callable
from loguru import logger

from app.core.settings.app import AppSettings


def create_start_app_handler(settings: AppSettings) -> Callable:
    async def start_app() -> None:
        ...
    
    return start_app


def create_stop_app_handler(settings: AppSettings) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        ...
    
    return stop_app