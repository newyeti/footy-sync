from dependency_injector import containers, providers

from app.internal.services import services
from app.internal.db.redis import RedisClient
from app.internal.db.mongo import MongoClient
from app.internal.db.repositorys import TeamRepository
from app.dependencies.constants import AppSettingsDependency, CommonsPathDependency

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
    
    api_service = providers.Factory(
        services.ApiService
    )
    
    team_repository = providers.Callable(
        TeamRepository,
        mongo_db
    )
    
    team_service = providers.Factory(
        services.TeamService,
        api_service=api_service,
        cache_service=cache_service,
        repository=team_repository
    )
    
    


