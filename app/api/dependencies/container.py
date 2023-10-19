from dependency_injector import containers, providers

from app.api.dependencies.cache import CacheService
from app.db.clients import redis, mongo
from app.services.rapid_api_service import RapidApiService
from app.services.teams import TeamService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    redis_pool = providers.Resource(
        redis.RedisClient.init_redis_pool,
        settings = config.redis_settings
    )
    
    mongo_db = providers.Singleton(
        mongo.MongoClient, settings=config.mongo_settings
    )
    
    cache_service = providers.Factory(
        CacheService,
        provider=redis_pool
    )

    api_service = providers.Factory(
        RapidApiService,
        cache_service=cache_service
    )

    team_service = providers.Factory(
        TeamService,
        cache_service=cache_service
    )
    