from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.standings import StandingsResponse
from app.models.domain.standings import Standings, TeamStanding
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
        logger.info(f"Standings:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self._rapid_api_service.settings.standings_endpoint
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span("standings.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        standings_obj = StandingsResponse.model_validate(api_response.response_data)
    
        logger.debug(f"standings count got: {len(standings_obj.response)}")
        
        return standings_obj
    
    def convert_to_domain(self, schema: StandingsResponse, season: int, league_id: int) -> list[Standings]:
        if len(schema.response) == 0:
            return []

        logger.debug("Converting Standings schema to domain model")
        
        league = schema.response[0].league
        team_standings: list[TeamStanding] = []
        
        for standing in league.standings[0]:
            team = {
                    "team_id": standing.team.id,
                    "team_name": standing.team.name,
                    "team_logo": standing.team.logo,
                }
            all = {
                    "played": standing.all.played,
                    "win": standing.all.win,
                    "draw": standing.all.draw,
                    "lose": standing.all.lose,
                    "goals": {
                        "goals_for": standing.all.goals.for_,
                        "goals_against": standing.all.goals.against,
                    },
                }
            home = {
                    "played": standing.home.played,
                    "win": standing.home.win,
                    "draw": standing.home.draw,
                    "lose": standing.home.lose,
                    "goals": {
                        "goals_for": standing.home.goals.for_,
                        "goals_against": standing.home.goals.against,
                    },
                }
            away = {
                    "played": standing.away.played,
                    "win": standing.away.win,
                    "draw": standing.away.draw,
                    "lose": standing.away.lose,
                    "goals": {
                        "goals_for": standing.away.goals.for_,
                        "goals_against": standing.away.goals.against,
                    },
                }
            
            team_standing: TeamStanding = {
                "rank": standing.rank,
                "team": team,
                "points": standing.points,
                "goals_diff": standing.goalsDiff,
                "group": standing.group,
                "form": standing.form,
                "status": standing.status,
                "description": standing.description,
                "all": all,
                "home": home,
                "away": away,
                "last_updated": standing.update,
            }
            
            team_standings.append(team_standing)
        
        standings: Standings = mapper.to(Standings).map(league, fields_mapping={
            "season": league.season,
            "league_id": league.id,
            "name": league.name,
            "country": league.country,
            "logo": league.logo,
            "flag": league.flag,
            "standings": team_standings,
        })
        
        return [standings]
        
    async def save_in_db(self, standings: list[Standings], season: int, league_id: int) -> None:
        logger.debug("Saving Standings domain models in database")
        with self.tracer.start_as_current_span("mongo.standings.save"):
            await self.__save_in_mongo(standings=standings)
    
    async def __save_in_mongo(self, standings: list[Standings]) -> None:
        logger.debug("Saving Standings domain models in mongo database")
        await self.standings_repository.update_bulk(standings=standings)
    
        
        
        
    