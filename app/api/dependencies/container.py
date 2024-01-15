from dependency_injector import containers, providers

from app.api.dependencies.cache import CacheService
from app.db.clients import redis, mongo, bigquery, kafka
from app.api.dependencies.rapid_api import RapidApiService
from app.services.team_service import TeamService
from app.services.fixture_service import FixtureService
from app.services.fixture_lineup_service import FixtureLineupService
from app.db.repositories.mongo import (
    team_repository,
    fixture_repository,
    fixture_lineups_repository
    )

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
    
    team_repository = providers.Factory(
        team_repository.TeamRepository,
        client=mongo_db
    )
    
    fixture_repository = providers.Factory(
        fixture_repository.FixtureRepository,
        client=mongo_db
    )
    
    fixture_lineup_repository = providers.Factory(
        fixture_lineups_repository.FixtureLineupRepository,
        client=mongo_db
    )

    team_service = providers.Factory(
        TeamService,
        rapid_api_service=rapid_api_service,
        team_repository=team_repository
        )
    
    fixture_service = providers.Factory(
        FixtureService,
        rapid_api_service=rapid_api_service,
        mongo_fixture_repository=fixture_repository
    )
    
    fixture_lineup_service = providers.Factory(
        FixtureLineupService,
        rapid_api_service=rapid_api_service,
        fixture_lineup_repository=fixture_lineup_repository
    )

    