from dependency_injector import containers, providers

from app.api.dependencies.cache import CacheService
from app.db.clients import redis, mongo
from app.api.dependencies.rapid_api import RapidApiService
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

    rapid_api_service = providers.Factory(
        RapidApiService,
        settings=config.rapid_api_settings,
        cache_service=cache_service
    )

    team_service = providers.Factory(
        TeamService,
        rapid_api_service=rapid_api_service,
        cache_service=cache_service
    )
    