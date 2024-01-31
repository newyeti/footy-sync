from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper
from abc import ABC
from  motor.motor_asyncio import AsyncIOMotorCursor
from app.services.base_service import BaseService
from app.models.schema.top_statistics import TopStatisticsResponse
from app.models.domain.top_statistics import Player
from app.api.dependencies.rapid_api import RapidApiService
from app.db.repositories.mongo.player_statistics_repository import PlayerStatisticsRepository
 
class TopPlayerService(BaseService, ABC):
    
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        self.tracer = trace.get_tracer(__name__)
        self.rapid_api_service = rapid_api_service
        self.player_statistics_repository = player_statistics_repository
        self.category=""
        self.api_endpoint = ""
        
    async def call_api(self, season: int, league_id: int, fixture_id: int = None) -> Any:
        logger.info(f"{self.category}: fetch_from_api - season={season}, league_id={league_id}")
        params = {
            "season": season,
            "league": league_id
        }
        with self.tracer.start_as_current_span(f"{self.category}.fetch.from.api"):
            api_response = await self.rapid_api_service.fetch_from_api(endpoint=self.api_endpoint, 
                                                params=params)
        
        Player_obj = TopStatisticsResponse.model_validate(api_response.response_data)
    
        logger.debug(f"Top Scorer count got: {len(Player_obj.response)}")
        
        return Player_obj
    
    def convert_to_domain(self, schema: TopStatisticsResponse) -> list[Player]:
        logger.debug(f"Converting {self.category} player schema to domain model")
        
        players: list[Player] = []
        
        for p in schema.response:
            statistic = p.statistics[0]
            player = mapper.to(Player).map(p, fields_mapping={
                "season": schema.parameters.season,
                "league_id": schema.parameters.league,
                "category": self.category,
                "player_id": p.player.id,
                "player_name": p.player.name,
                "detail": {
                    "firstname": p.player.firstname,
                    "lastname": p.player.lastname,
                    "birth": {
                        "date": p.player.birth.date,
                        "place": p.player.birth.place,
                        "country": p.player.birth.country,
                    },
                    "nationality": p.player.nationality,
                    "height": p.player.height,
                    "weight": p.player.height,
                    "injured": p.player.injured,
                    "photo": p.player.photo,
                },
                "team_id": statistic.team.id,
                "team_name": statistic.team.name,
                "games": {
                    "appearences": statistic.games.appearences,
                    "lineups": statistic.games.lineups,
                    "minutes": statistic.games.minutes,
                    "number": statistic.games.number,
                    "position": statistic.games.position,
                    "rating": statistic.games.rating,
                    "captain": statistic.games.captain,
                },
                "substitutes":  {
                    "in_": statistic.substitutes.in_,
                    "out": statistic.substitutes.out,
                    "bench": statistic.substitutes.bench, 
                },
                "shots": {
                    "total": statistic.shots.total,
                    "on": statistic.shots.on,
                },
                "goals": {
                    "total": statistic.goals.total,
                    "conceded": statistic.goals.conceded,
                    "assists": statistic.goals.assists,
                    "saves": statistic.goals.saves,
                },
                "passes": {
                    "total": statistic.passes.total,
                    "key": statistic.passes.key,
                    "accuracy": statistic.passes.accuracy,
                },
                "tackles": {
                    "total": statistic.tackles.total,
                    "blocks": statistic.tackles.blocks,
                    "interceptions": statistic.tackles.interceptions,
                },
                "duels": {
                    "total": statistic.duels.total,
                    "won": statistic.duels.won,
                },
                "dribbles": {
                    "attempts": statistic.dribbles.attempts,
                    "success": statistic.dribbles.success,
                    "past": statistic.dribbles.past,
                },
                "fouls": {
                    "drawn": statistic.fouls.drawn,
                    "committed": statistic.fouls.committed,
                },
                "cards": {
                    "yellow": statistic.cards.yellow,
                    "yellowred": statistic.cards.yellowred,
                    "red": statistic.cards.red,
                },
                "penalty": {
                    "won": statistic.penalty.won,
                    "committed": statistic.penalty.committed,
                    "scored": statistic.penalty.committed,
                    "missed": statistic.penalty.missed,
                    "saved": statistic.penalty.saved,
                }
            })
            players.append(player)            

        return players
        
    async def save_in_db(self, players: list[Player], season: int, league_id: int) -> None:
        logger.debug("Saving players domain models in database")
        
        with self.tracer.start_as_current_span(f"mongo.{self.category}.save"):
            await self.__save_in_mongo(players=players, season=season, league_id=league_id)
    
    async def __save_in_mongo(self, players: list[Player], season: int, league_id: int) -> None:
        logger.debug(f"Saving {self.category} domain models in mongo database")
        
        if players is None or len(players) == 0:
            logger.error("No data to save top_scorers.")
            return
        
        def convert_to_dict(players: list[Player]) -> dict[int, Player]:
            player_dict  = {}
            for p in players:
                player_dict[p["player_id"]] = Player.model_validate(p)
            return player_dict

        with self.tracer.start_as_current_span(f"mongo.{self.category}.find"):
            players_cursor: AsyncIOMotorCursor = self.player_statistics_repository.find({
                "season": season,
                "league_id": league_id,
                "category": self.category
            })
            players_in_db = await players_cursor.to_list(None) 
            
        existing_players: dict[int, Player] = convert_to_dict(players=players_in_db)
        players_to_update: list[Player] = []
        
        for p in players:
            if p.player_id in existing_players:
                del existing_players[p.player_id]
            players_to_update.append(p)
        
        logger.debug(f"{self.category} : Player to update: {len(players_to_update)}")
        logger.debug(f"{self.category} : Player to remove: {len(existing_players.keys())}")
        
        with self.tracer.start_as_current_span(f"mongo.{self.category}.update"):
            await self.player_statistics_repository.update_bulk(players=players_to_update)
        
        with self.tracer.start_as_current_span(f"mongo.{self.category}.delete"):
            await self.player_statistics_repository.delete_bulk(players=existing_players.values())