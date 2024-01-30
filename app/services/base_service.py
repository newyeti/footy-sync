from abc import ABC, abstractmethod
from typing import Any
from loguru import logger

from app.api.errors.service_error import ServiceException, RapidApiException
from app.api.errors.app_error import AppException

class BaseService(ABC):    
    async def execute(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        try:
            schema_obj = await self.call_api(season=season, league_id=league_id, fixture_id=fixture_id)
            if schema_obj:
                domain_obj = self.convert_to_domain(schema=schema_obj)
                if domain_obj:
                    await self.save_in_db(domain_obj, season=season, league_id=league_id)
        except RapidApiException as e:
            logger.error(e)
            raise ServiceException(name=e.name, api_url=e.api_url, message=e.message)
        except Exception as e:
            logger.error(e)
            raise AppException(message="Oops, something went wrong. Please try again later!")
        
        
    @abstractmethod
    async def call_api(self, season: int = None, league_id: int = None, fixture_id: int = None) -> Any:
        ...

    @abstractmethod
    def convert_to_domain(self, schema: Any) -> Any:
        ...

    @abstractmethod
    async def save_in_db(self, domain: list[Any], season: int = None, league_id: int = None) -> None:
        ...
    

class ApiService(ABC):
    @abstractmethod
    async def fetch_from_api(self,
                             endpoint: str,
                             season: int, 
                             league_id: int) -> Any:
        ...


        