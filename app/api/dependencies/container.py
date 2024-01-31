from dependency_injector import containers, providers

from app.api.dependencies.cache import CacheService
from app.db.clients import redis, mongo, bigquery, kafka
from app.api.dependencies.rapid_api import RapidApiService
from app.services.team_service import TeamService
from app.services.fixtures_service import FixtureService
from app.services.fixture_lineup_service import FixtureLineupService
from app.services.fixture_events_service import FixtureEventsService
from app.services.fixture_player_stats_service import FixturePlayerStatsService
from app.services.standings_service import StandingsService
from app.services.top_players_service import (
    TopScorersService,
    TopAssistsService,
    TopRedCardsService,
    TopYellowCardsService,
)
from app.services.top_players_service import TopAssistsService

from app.db.repositories.mongo import (
    player_statistics_repository,
    team_repository,
    fixture_repository,
    fixture_lineups_repository,
    fixture_events_repository,
    fixture_player_stat_repository,
    standings_repository,
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
    
    fixture_events_repository = providers.Factory(
        fixture_events_repository.FixtureEventRepository,
        client=mongo_db
    )
    
    fixture_player_stats_repository = providers.Factory(
        fixture_player_stat_repository.FixturePlayerStatRepository,
        client=mongo_db
    )
    
    standings_repository = providers.Factory(
        standings_repository.StandingsRepository,
        client=mongo_db
    )
    
    player_statistics_repository = providers.Factory(
        player_statistics_repository.PlayerStatisticsRepository,
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
        fixture_lineup_repository=fixture_lineup_repository,
        fixture_repository=fixture_repository
    )

    fixture_events_service = providers.Factory(
        FixtureEventsService,
        rapid_api_service=rapid_api_service,
        fixture_events_repository=fixture_events_repository,
        fixture_repository=fixture_repository
    )
    
    fixture_player_stats_service = providers.Factory(
        FixturePlayerStatsService,
        rapid_api_service=rapid_api_service,
        fixture_player_stats_repository=fixture_player_stats_repository,
        fixture_repository=fixture_repository
    )
    
    standings_service = providers.Factory(
        StandingsService,
        rapid_api_service=rapid_api_service,
        standings_repository=standings_repository
    )
    
    top_scorers_service = providers.Factory(
        TopScorersService,
        rapid_api_service=rapid_api_service,
        player_statistics_repository=player_statistics_repository
    )
    
    top_assists_service = providers.Factory(
        TopAssistsService,
        rapid_api_service=rapid_api_service,
        player_statistics_repository=player_statistics_repository
    )
    
    top_redcards_service = providers.Factory(
        TopRedCardsService,
        rapid_api_service=rapid_api_service,
        player_statistics_repository=player_statistics_repository
    )
    
    top_yellowcards_service = providers.Factory(
        TopYellowCardsService,
        rapid_api_service=rapid_api_service,
        player_statistics_repository=player_statistics_repository
    )
    