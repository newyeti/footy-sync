from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.standings import StandingsResponse
from app.models.domain.standings import Standings 
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.standings_repository import StandingsRepository

class StandingsService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 standings_repository: StandingsRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        self.standings_repository = standings_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.standings_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span("standings.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        standings_obj = StandingsResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture count got: {len(standings_obj.response)}")
        
        return standings_obj
    
    def convert_to_domain(self, schema: StandingsResponse) -> list[Standings]:
        logger.debug("Converting Fixture schema to domain model")
        return None
        
    async def save_in_db(self, standings: list[Standings]) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.standings.save"):
            await self.__save_in_mongo(standings=standings)
    
    async def __save_in_mongo(self, standings: list[Standings]) -> None:
        logger.debug("Saving Fixture domain models in mongo database")
        await self.standings_repository.update_bulk(standings=standings)
    
        
        
        
    