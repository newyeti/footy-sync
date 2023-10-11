from pydantic_settings import BaseSettings
from typing import Optional

class MongoSetting(BaseSettings):
    hostname: str
    username: str
    password: str
    
    class Config:
        env_prefix = "MONGO_"

class RedisSetting(BaseSettings):
    hostname: str
    port: int
    username: Optional[str | None]
    password: str
    ssl_enabled: bool = True

    class Config:
        env_prefix = "REDIS_"

class RapidApiSettings(BaseSettings):
    api_keys: str
    api_hostname: str = "api-football-v1.p.rapidapi.com"
    
    class Config:
        env_prefix = "RAPID_"
        
    def get_key() -> str:
        return "U4y3LniAIdmsh1SryySGibO7k8ELp1syFPvjsnpHOQNWAvpJAk"
        
class BigQuerySettings(BaseSettings):
    credential: str
    
    class Config:
        env_prefix = "BIGQUERY_"

class Settings(BaseSettings):
    app_name: str = "Footy-Sync"
    mongo: MongoSetting
    redis: RedisSetting
    bigquery: BigQuerySettings
    rapid_api: RapidApiSettings

