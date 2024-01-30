from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper
from  motor.motor_asyncio import AsyncIOMotorCursor
from app.services.base_service import BaseService
from app.models.schema.top_statistics import TopStatisticsResponse
from app.models.domain.top_statistics import Player, PlayerStatCategory
from app.api.dependencies.rapid_api import RapidApiService
from app.services.top_scorers_service import TopScorersService
from app.db.repositories.mongo.player_statistics_repository import PlayerStatisticsRepository
 
class TopAssistsService(TopScorersService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        super().__init__(rapid_api_service=rapid_api_service,
                         player_statistics_repository=player_statistics_repository)
        self.__tracer = trace.get_tracer(__name__)
        # self.__rapid_api_service = rapid_api_service
        # self.__player_statistics_repository = player_statistics_repository
        self.category=PlayerStatCategory.ASSIST.value
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"TopAssists:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self.rapid_api_service.settings.top_assists_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.__tracer.start_as_current_span("topassists.fetch.from.api"):
            api_response = await self.rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        Player_obj = TopStatisticsResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Top Assists count got: {len(Player_obj.response)}")
        
        return Player_obj
    
    