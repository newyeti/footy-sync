from typing import Any
from loguru import logger

from app.api.dependencies.cache import CacheService
from app.services.interface import IService


class TeamService(IService):

    def __init__(self, cache_service: CacheService) -> None:
        self.cache_service = cache_service

    async def sync(self, season: int, league_id: int) -> Any:
        logger.info(f"TeamService:fetch_from_api - season={season}, league_id={league_id}")

    
    async def save_in_db(self) -> None:
        ...
    
