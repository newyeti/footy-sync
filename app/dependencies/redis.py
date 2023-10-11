from typing import AsyncIterator
from aioredis import Redis, from_url


async def init_redis_pool(host: str, 
                          port: int, 
                          password: str,
                          max_connections: int) -> AsyncIterator[Redis]:
    session = Redis(host=host,
                    port=port,
                    password=password, 
                    encoding="utf-8",
                    decode_responses=True,
                    ssl=True,
                    ssl_cert_reqs="none",
                    max_connections=max_connections
                    )  
    yield session
    session.close()


