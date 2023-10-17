from dependency_injector import containers, providers

from app.api.dependencies.adapter import ContainderAdapter
from app.api.dependencies.cache import CacheService

class Container(containers.DeclarativeContainer):
    cache_service = providers.Factory(
        CacheService,
        provider=ContainderAdapter.redis_pool
    )
    