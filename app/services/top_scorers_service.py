from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.top_scorers import TopScorersResponse
from app.models.domain.top_scorers import TopScorers 
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.top_scorers_repository import TopScorersRepository

class TopScorersService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 top_scorers_repository: TopScorersRepository) -> None:
        self.__tracer = trace.get_tracer(__name__)
        self.__rapid_api_service = rapid_api_service
        self.__top_scorers_repository = top_scorers_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self.__rapid_api_service.settings.standings_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.__tracer.start_as_current_span("standings.fetch.from.api"):
            api_response = await self.__rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        standings_obj = TopScorersResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture count got: {len(standings_obj.response)}")
        
        return standings_obj
    
    def convert_to_domain(self, schema: TopScorersResponse) -> list[TopScorers]:
        logger.debug("Converting Fixture schema to domain model")
        return None
        
    async def save_in_db(self, top_scorers: list[TopScorers]) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.__tracer.start_as_current_span("mongo.standings.save"):
            await self.__save_in_mongo(top_scorers=top_scorers)
    
    async def __save_in_mongo(self, top_scorers: list[TopScorers]) -> None:
        logger.debug("Saving Fixture domain models in mongo database")
        await self.__top_scorers_repository.update_bulk(top_scorers==top_scorers)

        
    