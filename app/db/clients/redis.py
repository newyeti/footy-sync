from aioredis import Redis
from typing import AsyncIterator

from app.core.settings.base import RedisSetting

class RedisClient:
    async def init_redis_pool(settings: RedisSetting) -> AsyncIterator[Redis]:
        session = Redis(host=settings.hostname,
                        port=settings.port,
                        password=settings.password, 
                        encoding="utf-8",
                        decode_responses=True,
                        ssl=True,
                        ssl_cert_reqs="none",
                        max_connections=settings.max_connections
                        )  
        yield session
        session.close()
