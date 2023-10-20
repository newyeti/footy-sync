from typing import Any
from loguru import logger

from app.api.dependencies.cache import CacheService
from app.services.interface import IService
from app.api.dependencies.rapid_api import RapidApiService


class TeamService(IService):

    def __init__(self, 
                 rapid_api_service: RapidApiService,
                 cache_service: CacheService) -> None:
        self.rapid_api_service = rapid_api_service
        self.cache_service = cache_service

    async def sync(self, season: int, league_id: int) -> Any:
        logger.info(f"TeamService:fetch_from_api - season={season}, league_id={league_id}")
        api_response = await self.rapid_api_service.fetch_from_api(endpoint=self.rapid_api_service.settings.teams_endpoint, 
                                              season=season, 
                                              league_id=league_id)
        logger.debug(api_response.response_data)


    async def save_in_db(self) -> None:
        ...
    
