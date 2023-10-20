from typing import Any
from loguru import logger
import json

from app.api.dependencies.cache import CacheService
from app.services.interface import IService
from app.api.dependencies.rapid_api import RapidApiService
from app.models.schema.team import TeamInRapidApiResponse
from app.models.domain.team import Team


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
        teams_data = json.dumps(api_response.response_data)
        logger.debug(f"Team Response Data: {teams_data}")
        if teams_data:
            teams = self.convert_to_domain(teams_data)
            logger.debug(f"Teams domain data: {teams}")
            

    def convert_to_domain(self, schema: TeamInRapidApiResponse) -> list[Team]:
        ...


    async def save_in_db(self, domain: Team) -> None:
        ...
    
