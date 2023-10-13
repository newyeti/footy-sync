from aioredis import Redis
from app.dependencies.logger import get_logger

logger = get_logger(__name__)

class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
    
    async def redis_conn_test(self) -> str:
        await self._redis.set("test_key", "success")
        value = await self._redis.get("test_key")
        await self._redis.delete("test_key")
        return value