from enum import Enum
from pydantic_settings import BaseSettings

class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod
    
    class Config:
        env_file = "../.env"
    

class RapidApiSetting(BaseSettings):
    api_keys: tuple
    api_hostname: str = "api-football-v1.p.rapidapi.com"
    teams_endpoint: str = "/v3/teams"
    fixtures_endpoint: str = "/v3/fixtures"
    fixtures_lineups_endpoint: str = "/v3/fixtures/lineups"
    fixtures_events_endpoint: str = "v3/fixtures/events"
    fixtures_player_stat_endpoing: str = "v3/fixtures/players"
    standings_endpoint: str = "v3/standings"
    top_scorers_endpoing: str = "/v3/players/topscorers"
    daily_limit: int = 100
    cache_key: str = "FS::DAILY_RAPID_API_CALLS"
    cache_key_expiry_in_days: int = 7
    
    class Config:
        env_prefix = "RAPID_"

class AuthSettings(BaseSettings):
    domain: str
    api_audience: str
    issuer: str
    algorithm: str
    
    class Config:
        env_prefix = "AUTH0_"

