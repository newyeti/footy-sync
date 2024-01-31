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
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}, fixture_id={fixture_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_events_endpoint
        params = {
            "fixture": fixture_id,
        }
        with self.tracer.start_as_current_span("fixture_events.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        fixture_events_obj = FixtureEventResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture Events count got: {len(fixture_events_obj.response)}")
        
        return fixture_events_obj
    
    def convert_to_domain(self, schema: FixtureEventResponse, season: int, league_id: int) -> list[FixtureEvent]:
        logger.debug("Converting Fixture Events schema to domain model")
        
        fixture_events : list[FixtureEvent] = []
        
        for e in schema.response:
            event = mapper.to(FixtureEvent).map(
                schema, fields_mapping={
                    "season": season,
                    "league_id": league_id,
                    "fixture_id": schema.parameters.fixture,
                    "elapsed": e.time.elapsed,
                    "elapsed_plus": e.time.extra,
                    "team_id": e.team.id,
                    "team_name": e.team.name,
                    "player_id": e.player.id,
                    "player_name": e.player.name,
                    "assist_player_id": e.assist.id,
                    "assist_player_name": e.assist.name,
                    "event_type": e.type,
                    "detail": e.detail,
                    "comments": e.comments,
                }
            )
            fixture_events.append(event)
        
        return fixture_events
        
    async def save_in_db(self, events: list[FixtureEvent], season: int = None, league_id: int = None) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.fixture_events.save"):
            await self.__save_in_mongo(events=events)
    
    async def __save_in_mongo(self, events: list[FixtureEvent]) -> None:
        if len(events) == 0:
            logger.error("Fixture events is not available")
            return

        fixture_event = events[0]
        fixture_filter = {
            "season": fixture_event.season,
            "league_id": fixture_event.league_id,
            "fixture_id": fixture_event.fixture_id,
        }
        
        logger.info(f"Finding Fixture {fixture_filter} in mongo database")
        fixture = await self.fixture_repository.findOne(filter=fixture_filter)
        
        if fixture is None:
            logger.error(f"Fixture for {fixture_filter} is not available.")
        else:
            for event in events:
                event.event_date = fixture.event_date
        
            logger.debug("Saving Fixture domain models in mongo database")
            await self.fixture_events_repository.update_bulk(events=events)
    
        
        
        
    