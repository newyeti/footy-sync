import os

from loguru import logger

from app.db.clients.mongo import MongoClient
from app.db.errors import DBConnectionError
from app.api.dependencies.cache import CacheService

async def test_mongodb_connection(mongo_db: MongoClient):
    logger.info("Connecting to MongoDB")
    logger.debug(f"mongodb instance: {mongo_db}")
    try:
        is_connected = await mongo_db.is_connected()
        logger.debug(is_connected)
        logger.info(f"Connected to MongoDB -  {os.getenv('APP_ENV', 'DEV').upper()} environment!")
    except Exception as e:
        raise DBConnectionError(e)


async def stop_mongodb(mongo_db: MongoClient):
    logger.info("Closing connection to MongoDB")
    try:
        mongo_db.close()
        logger.info(
            logger.info("MongoDB connection closed")
        )
    except Exception as e:
        raise DBConnectionError(e)
    

async def test_cache_service(cache_service: CacheService):
    logger.info("Connecting to Cache Provider")
    try:
        await cache_service.set("test_key", '{"conn": "success"}')
        value = await cache_service.get("test_key")
        await cache_service.delete("test_key")
        logger.debug(f"Cache Provider: {value}")
        logger.info(f"Connected to Cache Provider - {os.getenv('APP_ENV', 'DEV').upper()} environment!")
    except Exception as e:
        raise DBConnectionError(e)
