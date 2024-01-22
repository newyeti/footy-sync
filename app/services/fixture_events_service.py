from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture_event import FixtureEventResponse
from app.models.domain.fixture_event import FixtureEvent 
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.fixture_repository import FixtureRepository
from app.db.repositories.mongo.fixture_events_repository import FixtureEventRepository


class FixtureEventsService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 fixture_events_repository: FixtureEventRepository,
                 fixture_repository: FixtureRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        self.fixture_events_repository = fixture_events_repository
        self.fixture_repository = fixture_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_events_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span("fixture_events.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        fixture_events_obj = FixtureEventResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture count got: {len(fixture_events_obj.response)}")
        
        return fixture_events_obj
    
    def convert_to_domain(self, schema: FixtureEventResponse) -> list[FixtureEvent]:
        logger.debug("Converting Fixture schema to domain model")
        return None
        
    async def save_in_db(self, fixtures: list[FixtureEvent]) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.fixture_events.save"):
            await self.__save_in_mongo(fixtures=fixtures)
    
    async def __save_in_mongo(self, events: list[FixtureEvent]) -> None:
        logger.debug("Saving Fixture domain models in mongo database")
        await self.fixture_event_repository.update_bulk(fixtures=events)
    
        
        
        
    