from dependency_injector import containers, providers

from . import services
from app.internal.db.redis_client import RedisClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.internal.db.mongo_client import MongoClient
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

    service = providers.Factory(
        services.Service,
        redis=redis_pool
    )
    
    team = providers.Callable(
        TeamRepository,
        mongo_db
    )

