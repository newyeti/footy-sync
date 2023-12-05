import os

# from loguru import logger
import logging
from app.db.clients.mongo import MongoClient
from app.db.clients.bigquery import BigQueryClient
from app.db.errors import DBConnectionError
from app.api.dependencies.cache import CacheService

async def test_mongodb_connection(mongo_db: MongoClient):
    logging.info("Connecting to MongoDB")
    logging.debug(f"mongodb instance: {mongo_db}")
    try:
        is_connected = await mongo_db.is_connected()
        logging.debug(is_connected)
        logging.info(f"Connected to MongoDB -  {os.getenv('APP_ENV', 'DEV').upper()} environment!")
    except Exception as e:
        raise DBConnectionError(e)


async def stop_mongodb(mongo_db: MongoClient):
    logging.info("Closing connection to MongoDB")
    try:
        mongo_db.close()
        logging.info(
            logging.info("MongoDB connection closed")
        )
    except Exception as e:
        raise DBConnectionError(e)
    

async def test_cache_service(cache_service: CacheService):
    logging.info("Connecting to Cache Provider")
    try:
        await cache_service.set("test_key", '{"conn": "success"}')
        value = await cache_service.get("test_key")
        await cache_service.delete("test_key")
        logging.debug(f"Cache Provider: {value}")
        logging.info(f"Connected to Cache Provider - {os.getenv('APP_ENV', 'DEV').upper()} environment!")
    except Exception as e:
        raise DBConnectionError(e)


async def test_bigquery_connection(bigquery_client: BigQueryClient):
    logging.info("Connecting to Bigquery")
    try:
        if bigquery_client.isconnected():
            logging.info("Connected to BigQuery")
        else:
            raise DBConnectionError(
                "Connection could not be established with BigQuery")
    except Exception as e:
        raise DBConnectionError(e)
