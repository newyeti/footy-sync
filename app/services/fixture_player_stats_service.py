from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper

from app.services.base_service import BaseService
from app.models.schema.fixture_player_stat import FixtureStatResponse
from app.models.domain.fixture_player_stat import FixturePlayerStatistics 
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
            "fixture": fixture_id
        }
        with self.tracer.start_as_current_span("fixture_events.fetch.from.api"):
            api_response = await self._rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                                params=params)
        
        fixture_player_stats_obj = FixtureStatResponse.model_validate(api_response.response_data)
        logger.debug(f"Fixture count got: {len(fixture_player_stats_obj.response)}")
        
        return fixture_player_stats_obj
    
    def convert_to_domain(self, schema: FixtureStatResponse, season: int, league_id: int) -> list[FixturePlayerStatistics]:
        logger.debug("Converting Fixture schema to domain model")
        fixture_statistics: list[FixturePlayerStatistics] = []
        
        for stat in schema.response:
            for player in stat.players:
                statistics = player.statistics[0]
                player_stat = mapper.to(FixturePlayerStatistics).map(stat, fields_mapping={
                    "season": season,
                    "league_id": league_id,
                    "fixture_id": schema.parameters.fixture,
                    "team_id": stat.team.id,
                    "team_name": stat.team.name,
                    "player_id": player.player.id,
                    "player_name": player.player.name,
                    "number": statistics.games.number,
                    "position": statistics.games.position,
                    "rating": statistics.games.rating,
                    "minutes_played": statistics.games.minutes,
                    "captain": statistics.games.captain,
                    "substitute": statistics.games.substitute,
                    "offsides": statistics.offsides,
                    "shots": {
                        "total": statistics.shots.total,
                        "on": statistics.shots.on,
                    },
                    "goals": {
                        "total": statistics.goals.total,
                        "conceded": statistics.goals.conceded,
                        "assists": statistics.goals.assists,
                        "saves": statistics.goals.saves,
                    },
                    "passes": {
                        "total": statistics.passes.total,
                        "key": statistics.passes.key,
                        "accuracy": statistics.passes.accuracy,
                    },
                    "tackles": {
                        "total": statistics.tackles.total,
                        "blocks": statistics.tackles.blocks,
                        "interceptions": statistics.tackles.interceptions,
                    },
                    "duels": {
                        "total": statistics.duels.total,
                        "won": statistics.duels.won,
                    },
                    "dribbles": {
                        "attempts": statistics.dribbles.attempts,
                        "success": statistics.dribbles.success,
                        "past": statistics.dribbles.past,
                    }, 
                    "fouls": {
                        "drawn": statistics.fouls.drawn,
                        "committed": statistics.fouls.committed,
                    },
                    "cards": {
                        "yellow": statistics.cards.yellow,
                        "red": statistics.cards.red,
                    },
                    "penalty": {
                        "won": statistics.penalty.won,
                        "committed": statistics.penalty.committed,
                        "success": statistics.penalty.success,
                        "saved": statistics.penalty.saved,
                    },
                })
                fixture_statistics.append(player_stat)
        
        return fixture_statistics
        
    async def save_in_db(self, fixture_player_stats: list[FixturePlayerStatistics], season: int, league_id: int) -> None:
        logger.debug("Saving Fixture domain models in database")
        with self.tracer.start_as_current_span("mongo.fixture_player_stats.save"):
            await self.__save_in_mongo(fixture_player_stats=fixture_player_stats)
    
    async def __save_in_mongo(self, fixture_player_stats: list[FixturePlayerStatistics]) -> None:
        if len(fixture_player_stats) == 0:
            logger.error("Fixture lineup is not available")
            return
        
        fixture_stat = fixture_player_stats[0]
        fixture_filter = {
            "season": fixture_stat.season,
            "league_id": fixture_stat.league_id,
            "fixture_id": fixture_stat.fixture_id,
        }
        
        logger.info(f"Finding Fixture {fixture_filter} in mongo database")
        fixture = await self.fixture_repository.findOne(filter=fixture_filter)
        
        if fixture is None:
            logger.error(f"Fixture for {fixture_filter} is not available.")
        else:
            logger.info("Saving Fixture Player Statistics domain models in mongo database")
            for player_stat in fixture_player_stats:
                player_stat.event_date = fixture.event_date
        
            await self.fixture_player_stats_repository.update_bulk(fixture_player_stats=fixture_player_stats)
    
        
        
        
    