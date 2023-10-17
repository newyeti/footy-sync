from enum import Enum
from typing import Optional

from pydantic_settings import BaseSettings

class MongoSetting(BaseSettings):
    hostname: str
    username: str
    password: str
    db: str
    
    def get_uri(self) -> str:
        return f"mongodb+srv://{self.username}:{self.password}@{self.hostname}/?retryWrites=true&w=majority"
    
    class Config:
        env_prefix = "MONGO_"

class RedisSetting(BaseSettings):
    hostname: str
    port: int
    username: Optional[str | None]
    password: str
    ssl_enabled: bool = True
    max_connections: int = 50

    class Config:
        env_prefix = "REDIS_"

class RapidApiSettings(BaseSettings):
    api_keys: str
    api_hostname: str = "api-football-v1.p.rapidapi.com"
    
    class Config:
        env_prefix = "RAPID_"
        
class BigQuerySettings(BaseSettings):
    credential: str
    
    class Config:
        env_prefix = "BIGQUERY_"


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod
    
    class Config:
        env_file = ".env"
    

