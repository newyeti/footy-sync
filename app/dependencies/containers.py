from dependency_injector import containers, providers

from ..internal.services import services
from app.internal.db.redis import RedisClient
from app.internal.db.mongo import MongoClient
from app.internal.db.repositorys import TeamRepository

class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    redis_pool = providers.Resource(
        RedisClient.init_redis_pool,
        settings = config.redis_settings
    )
    
    mongo_db = providers.Singleton(
        MongoClient, uri=config.mongo_uri, settings=config.mongo_settings
    )

    cache_service = providers.Factory(
        services.CacheService,
        provider=redis_pool
    )
    
    team_service = providers.Factory(
        services.TeamService,
        cache_service=cache_service
    )
    
    team_repository = providers.Callable(
        TeamRepository,
        mongo_db
    )

