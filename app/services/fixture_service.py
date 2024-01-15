from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture import FixtureResponse
from app.models.domain.fixture import Fixture, Team, Goal, Score
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.fixture_repository import FixtureRepository as MongoFixtureRepository

class FixtureService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 mongo_fixture_repository: MongoFixtureRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        self.mongo_fixture_repository = mongo_fixture_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"Fixture:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span("fixtures.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
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
            
            score = {}
            if f.score.halftime.home is not None or f.score.halftime.away is not None:
                score["half_time"] = f"{f.score.halftime.home}-{f.score.halftime.away}"
            if f.score.fulltime.home is not None or f.score.fulltime.away is not None:
                score["full_time"] = f"{f.score.fulltime.home}-{f.score.fulltime.away}"
            if f.score.extratime.home is not None or f.score.extratime.away is not None:
                score["extra_time"] = f"{f.score.extratime.home}-{f.score.extratime.away}"
            if f.score.penalty.home is not None or f.score.penalty.away is not None:
                score["penalty"] = f"{f.score.penalty.home}-{f.score.penalty.away}"
            
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
        
    async def save_in_db(self, fixtures: list[Fixture]) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.team.save"):
            await self.__save_in_mongo(fixtures=fixtures)
    
    async def __save_in_mongo(self, fixtures: list[Fixture]) -> None:
        logger.debug("Saving Fixture domain models in mongo database")
        await self.mongo_fixture_repository.update_bulk(fixtures=fixtures)
    
        
        
        
    