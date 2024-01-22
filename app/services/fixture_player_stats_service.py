from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture_player_stat import FixturePlayerStatResponse
from app.models.domain.fixture_player_stat import FixturePlayerStat 
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.fixture_player_stat_repository import FixturePlayerStatRepository
from app.db.repositories.mongo.fixture_repository import FixtureRepository


class FixturePlayerStatsService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 fixture_player_stats_repository: FixturePlayerStatRepository,
                 fixture_repository: FixtureRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        self.fixture_player_stats_repository = fixture_player_stats_repository
        self.fixture_repository = fixture_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_player_stat_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span("fixture_events.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        fixture_player_stats_obj = FixturePlayerStatResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture count got: {len(fixture_player_stats_obj.response)}")
        
        return fixture_player_stats_obj
    
    def convert_to_domain(self, schema: FixturePlayerStatResponse) -> list[FixturePlayerStat]:
        logger.debug("Converting Fixture schema to domain model")
        return None
        
    async def save_in_db(self, player_stats: list[FixturePlayerStat]) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.fixture_player_stats.save"):
            await self.__save_in_mongo(fixtures=player_stats)
    
    async def __save_in_mongo(self, player_stats: list[FixturePlayerStat]) -> None:
        logger.debug("Saving Fixture domain models in mongo database")
        await self.fixture_player_stats_repository.update_bulk(player_stats=player_stats)
    
        
        
        
    