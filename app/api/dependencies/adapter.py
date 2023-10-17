from dependency_injector import providers, containers

from app.db.clients import redis, mongo


class ContainderAdapter(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    redis_pool = providers.Resource(
        redis.RedisClient.init_redis_pool,
        settings = config.redis_settings
    )
    
    mongo_db = providers.Singleton(
        mongo.MongoClient, settings=config.mongo_settings
    )
    
