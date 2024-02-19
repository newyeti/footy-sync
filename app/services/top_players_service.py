from typing import Any
from loguru import logger
from opentelemetry import trace
from automapper import mapper
from  motor.motor_asyncio import AsyncIOMotorCursor
from app.models.domain.top_statistics import PlayerStatCategory
from app.api.dependencies.rapid_api import RapidApiService
from app.services.top_players_base_service import TopPlayerService
from app.db.repositories.mongo.player_statistics_repository import PlayerStatisticsRepository


class TopScorersService(TopPlayerService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        super().__init__(rapid_api_service=rapid_api_service,
                         player_statistics_repository=player_statistics_repository)
        self.tracer = trace.get_tracer(__name__)
        self.category=PlayerStatCategory.SCORER.value
        self.api_endpoint = self.rapid_api_service.settings.top_scorers_endpoint
         
class TopAssistsService(TopPlayerService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        super().__init__(rapid_api_service=rapid_api_service,
                         player_statistics_repository=player_statistics_repository)
        self.tracer = trace.get_tracer(__name__)
        self.category=PlayerStatCategory.ASSIST.value
        self.api_endpoint = self.rapid_api_service.settings.top_assists_endpoint

class TopRedCardsService(TopPlayerService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        super().__init__(rapid_api_service=rapid_api_service,
                         player_statistics_repository=player_statistics_repository)
        self.tracer = trace.get_tracer(__name__)
        self.category=PlayerStatCategory.RED_CARD.value
        self.api_endpoint = self.rapid_api_service.settings.top_red_cards_endpoint 

class TopYellowCardsService(TopPlayerService):
    def __init__(self,
                 rapid_api_service: RapidApiService,
                 player_statistics_repository: PlayerStatisticsRepository) -> None:
        super().__init__(rapid_api_service=rapid_api_service,
                         player_statistics_repository=player_statistics_repository)
        self.tracer = trace.get_tracer(__name__)
        self.category=PlayerStatCategory.YELLOW_CARD.value
        self.api_endpoint = self.rapid_api_service.settings.top_yellow_cards_endpoint