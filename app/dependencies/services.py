from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
    
    async def redis_conn_test(self) -> str:
        await self._redis.set("test_key", "success")
        value = await self._redis.get("test_key")
        await self._redis.delete("test_key")
        return value