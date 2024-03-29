from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture_lineup import FixtureLineUpResponse, Players, Player, Color
from app.models.domain.fixture_lineup import FixtureLineup
from app.models.domain.fixture import Fixture
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.fixture_lineups_repository import FixtureLineupRepository
from app.db.repositories.mongo.fixture_repository import FixtureRepository

class FixtureLineupService(BaseService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 fixture_lineup_repository: FixtureLineupRepository,
                 fixture_repository: FixtureRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self._rapid_api_service = rapid_api_service
        self.fixture_lineup_repository = fixture_lineup_repository
        self.fixture_repository = fixture_repository
        
    async def call_api(self, season: int, league_id: int, fixture_id: int) -> Any:
        logger.info(f"Fixture_Lineup:fetch_from_api - season={season}, league_id={league_id} - fixture_id={fixture_id}")
        api_endpoint = self._rapid_api_service.settings.fixtures_lineups_endpoint
        params = {
            "fixture": fixture_id
        }
        with self.tracer.start_as_current_span("fixtures.lineups.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        fixture_lineup_obj = FixtureLineUpResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Fixture Lineup count got: {len(fixture_lineup_obj.response)}")
        
        return fixture_lineup_obj
    
    def convert_to_domain(self, schema: FixtureLineUpResponse, season: int, league_id: int) -> list[FixtureLineup]:
        logger.debug("Converting Fixture Lineup schema to domain model")
        
        fixture_lineups : list[FixtureLineup] = []
        for lineup in schema.response:
            
            startPlayers: list[Player] = self.__map_players(lineup.startXI)
            substitutePlayers: list[Player] = self.__map_players(lineup.substitutes)
            
            fixture_lineup = mapper.to(FixtureLineup).map(schema, fields_mapping={
                "season": season,
                "league_id": league_id,
                "fixture_id": schema.parameters.fixture,
                "team_id": lineup.team.id,
                "team_name": lineup.team.name,
                "team_player_color": self.__map_colors(lineup.team.colors.player),
                "team_goalkeeper_color": self.__map_colors(lineup.team.colors.goalkeeper),
                "team_logo": lineup.team.logo,
                "coach_id": lineup.coach.id,
                "coach_name": lineup.coach.name,
                "formation": lineup.formation,
                "startingXI": startPlayers,
                "substitutes": substitutePlayers,
            })
            fixture_lineups.append(fixture_lineup)
    
        return fixture_lineups
        
    async def save_in_db(self, lineups: list[FixtureLineup], season: int = None, league_id: int = None) -> None:
        logger.debug("Saving Fixture Lineup domain models in database")
        with self.tracer.start_as_current_span("mongo.team.save"):
            await self.__save_in_mongo(lineups=lineups)
    
    async def __save_in_mongo(self, lineups: list[FixtureLineup]) -> None:
        if len(lineups) == 0:
            logger.error("Fixture lineup is not available")
            return
        
        fixture_lineup = lineups[0]
        fixture_filter = {
            "season": fixture_lineup.season,
            "league_id": fixture_lineup.league_id,
            "fixture_id": fixture_lineup.fixture_id,
        }
        
        logger.info(f"Finding Fixture {fixture_filter} in mongo database")
        fixture = await self.fixture_repository.findOne(filter=fixture_filter)
        
        if fixture is None:
            logger.error(f"Fixture for {fixture_filter} is not available.")
        else:
            logger.info("Saving Fixture linue up domain models in mongo database")
            for lineup in lineups:
                lineup.event_date = fixture.event_date
            
            await self.fixture_lineup_repository.update_bulk(lineups=lineups)


    def __map_players(self, players: list[Players]) -> list[Player]:
        player_list : list[Player] = []
        for p in players:
            player = {
                "player_id": p.player.id,
                "player_name": p.player.name,
                "number": p.player.number,
                "pos": p.player.pos,
                "grid": p.player.grid
            }
            player_list.append(player)
        
        return player_list
    
    def __map_colors(self, color: Color) -> str:
        return f"{color.primary}|{color.number}|{color.border}"