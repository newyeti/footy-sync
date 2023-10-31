from abc import ABC, abstractmethod
from typing import Any
from loguru import logger

from app.api.errors.service_error import ServiceException, RapidApiException
from app.api.errors.app_error import AppException

class BaseService(ABC):

    async def sync_template(self, season: int, league_id: int) -> Any:
        try:
            schema_obj = await self.call_api(season=season, league_id=league_id)
            domain_obj = self.convert_to_domain(schema=schema_obj)
            await self.save_in_db(domain_obj)
        except RapidApiException as e:
            logger.error(e)
            raise ServiceException(e)
        except Exception as e:
            logger.error(e)
            raise AppException(message="Oops, something went wrong. Please try again later!")
        
        
    @abstractmethod
    async def call_api(self, season: int, league_id: int) -> Any:
        ...

    @abstractmethod
    def convert_to_domain(self, schema: Any) -> Any:
        ...

    @abstractmethod
    async def save_in_db(self, domain: list[Any]) -> None:
        ...
    

class ApiService(ABC):
    @abstractmethod
    async def fetch_from_api(self,
                             endpoint: str,
                             season: int, 
                             league_id: int) -> Any:
        ...