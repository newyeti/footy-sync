from enum import Enum
from pydantic_settings import BaseSettings

class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod
    
    class Config:
        env_file = ".env"
    

class RapidApiSetting(BaseSettings):
    api_keys: str
    api_hostname: str = "api-football-v1.p.rapidapi.com"
    teams_endpoint: str = "/v3/teams"
    daily_limit: int = 100
    cache_key: str = "FS::DAILY_RAPID_API_CALLS"
    cache_key_expiry_in_days: int = 7
    
    class Config:
        env_prefix = "RAPID_"
