from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture import FixtureResponse
from app.models.domain.fixture import Fixture, Team, Goal, Score
from app.api.dependencies.rapid_api import RapidApiService

class FixtureService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        
    
    async def call_api(self, season: int, league_id: int) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_endpoint
        with self.tracer.start_as_current_span("fixtures.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                season=season, 
                                                league_id=league_id)
        
        fixtures_obj = FixtureResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture count got: {len(fixtures_obj.response)}")
        
        return fixtures_obj
    
    def convert_to_domain(self, schema: FixtureResponse) -> list[Fixture]:
        logger.debug("Converting Fixture schema to domain model")
        
        fixtures : list[Fixture] = []
        for f in schema.response:
            home_team = {
                "team_id": f.teams.home.id,
                "team_name": f.teams.home.name,
                "team_logo": f.teams.home.logo,
            }
            
            away_team = {
                 "team_id": f.teams.away.id,
                "team_name": f.teams.away.name,
                "team_logo": f.teams.away.logo, 
            }
            
            goals = {
                "home_team": f.goals.home,
                "away_team": f.goals.away,
            }
            
            score = {
                "half_time": f"{f.score.halftime.home}-{f.score.halftime.away}",
                "full_time": f"{f.score.fulltime.home}-{f.score.fulltime.away}",
                "extra_time": f"{f.score.halftime.home}-{f.score.halftime.away}",
                "penalty": f"{f.score.fulltime.home}-{f.score.fulltime.away}",
            }
            
            fixture = mapper.to(Fixture).map(schema, fields_mapping={
                "season": schema.parameters.season,
                "league_id": schema.parameters.league,
                "fixture_id": f.fixture.id,
                "league_name": f.league.name,
                "event_date": f.fixture.date,
                "first_half_start": f.fixture.periods.first,
                "second_half_start": f.fixture.periods.second,
                "round": f.league.round,
                "status": f.fixture.status.short,
                "elapsed": f.fixture.status.elapsed,
                "stadium": f.fixture.venue.name,
                "city": f.fixture.venue.city,
                "referee": f.fixture.referee,
                "home_team": home_team,
                "away_team": away_team,
                "goals": goals,
                "score": score
            })
            fixtures.append(fixture)
    
        return fixtures
        
        
    async def save_in_db(self, fixture: list[Fixture]) -> None:
        logger.debug("Saving Fixture domain models in database")
        
    