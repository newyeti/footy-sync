from abc import ABC, abstractmethod
from typing import Any
from loguru import logger

from app.api.errors.service_error import ServiceException
from app.api.errors.app_error import AppException

class IService(ABC):

    async def sync_template(self, season: int, league_id: int) -> Any:
        try:
            schema_obj = await self.call_api(season=season, league_id=league_id)
            domain_obj = self.convert_to_domain(schema=schema_obj)
            await self.save_in_db(domain=domain_obj)
        except ValueError as e:
            logger.error(e)
            raise ServiceException(name=e.args[1], api_url=e.args[2], message=e.args[0])
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
    async def save_in_db(self, domain: Any) -> None:
        ...
    

class ApiService(ABC):
    @abstractmethod
    async def fetch_from_api(self,
                             endpoint: str,
                             season: int, 
                             league_id: int) -> Any:
        ...