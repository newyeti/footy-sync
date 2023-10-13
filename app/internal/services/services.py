from aioredis import Redis
from app.dependencies.logger import get_logger

import json

logger = get_logger(__name__)


class CacheService:
    def __init__(self, provider: Redis) -> None:
        self.__provider = provider

    async def get(self, key):
        value = await self.__provider.get(str(key))
        return json.loads(value) if value else None

    async def set(self, key, value, exp=None):
        return await self.__provider.set(str(key), value, exp)

    async def delete(self, key):
        return await self.__provider.delete(str(key))

    async def get_all(self):
        keys = await self.__provider.keys("*")
        return [json.loads(await self.__provider.get(key)) for key in keys]


class TeamService:
    def __init__(self, cache_service: CacheService) -> None:
        self._cache_service = cache_service
    
    async def redis_conn_test(self) -> str:
        await self._cache_service.set("test_key", '{"conn": "success"}')
        value = await self._redis.get("test_key")
        await self._redis.delete("test_key")
        return value
    


