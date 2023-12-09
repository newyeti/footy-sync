import logging

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    is_debug: bool = True
    title: str = "Dev - Footy Data Sync App"
    logging_level: int = logging.DEBUG
    
    class Config:
        env_file = "../.env"
