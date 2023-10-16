import logging
import sys

from typing import Tuple, List, Dict, Any
from loguru import logger

from app.core.settings.base import BaseAppSettings
from app.core.logging import InterceptHandler


class AppSettings(BaseAppSettings):
    is_debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "Footy Data Sync App"
    version: str = "0.0.1"
    api_prefix: str = ""
    
    allowed_hosts: List[str] = ["*"]
    
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
      
    class Config:
        validate_assignment = True
        
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.is_debug,
            "docs_url": self.docs_url,
            "apenapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "title": self.title,
            "version": self.version
        }
    
    
    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for name in self.loggers:
            logging_logger = logging.getLogger(name=name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]
    
        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
    
