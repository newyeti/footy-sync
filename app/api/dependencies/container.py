from dependency_injector import containers, providers

from app.api.dependencies.cache import CacheService
from app.db.clients import redis, mongo, bigquery, kafka
from app.api.dependencies.rapid_api import RapidApiService
from app.services.team_service import TeamService
from app.services.fixture_service import FixtureService
from app.db.repositories.mongo import (
    team_repository as mongo_team_repository,
    fixture_repository as mongo_fixture_repository)

from app.db.repositories.bigquery.team_repository import TeamRepository as BigQueryTeamRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    redis_pool = providers.Resource(
        redis.RedisClient.init_redis_pool,
        settings = config.redis_settings
    )
    
    mongo_db = providers.Singleton(
        mongo.MongoClient, settings=config.mongo_settings
    )
    
    bigquery = providers.Singleton(
        bigquery.BigQueryClient, settings=config.bigquery_settings
    )

    cache_service = providers.Factory(
        CacheService,
        provider=redis_pool
    )
    
    kafka_client = providers.Singleton(
        kafka.KafkaClient, settings=config.kafka_settings
    )

    rapid_api_service = providers.Factory(
        RapidApiService,
        settings=config.rapid_api_settings,
        cache_service=cache_service
    )
    
    mongo_team_repository = providers.Factory(
        mongo_team_repository.TeamRepository,
        client=mongo_db
    )
    
    mongo_fixture_repository = providers.Factory(
        mongo_fixture_repository.FixtureRepository,
        client=mongo_db
    )

    bigquery_team_repository = providers.Factory(
        BigQueryTeamRepository,
        client=bigquery
    )

    team_service = providers.Factory(
        TeamService,
        rapid_api_service=rapid_api_service,
        cache_service=cache_service,
        mongo_team_repository=mongo_team_repository,
        bigquery_team_repository=bigquery_team_repository
    )
    
    fixture_service = providers.Factory(
        FixtureService,
        rapid_api_service=rapid_api_service,
        mongo_fixture_repository=mongo_fixture_repository,
        kafka_client=kafka_client
    )
    
    