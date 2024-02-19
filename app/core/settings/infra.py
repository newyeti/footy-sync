from pydantic_settings import BaseSettings
from typing import Optional


class MongoSettings(BaseSettings):
    hostname: str
    username: str
    password: str
    db: str
    
    def get_uri(self) -> str:
        return f"mongodb+srv://{self.username}:{self.password}@{self.hostname}/?retryWrites=true&w=majority"
    
    class Config:
        env_prefix = "MONGO_"

class RedisSettings(BaseSettings):
    hostname: str
    port: int
    username: Optional[str | None]
    password: str
    ssl_enabled: bool = True
    max_connections: int = 50

    class Config:
        env_prefix = "REDIS_"

        
class BigQuerySettings(BaseSettings):
    project: str
    credential: str
    dataset: str
    
    class Config:
        env_prefix = "BIGQUERY_"

class KafkaSettings(BaseSettings):
    bootstrap_servers: str
    username: str
    password: str
    sasl_mechanism: str = "SCRAM-SHA-256"
    security_protocol: str = "SASL_SSL"
    client_id: str = "footy-sync"
    
    class Config:
        env_prefix = "KAFKA_"


class InfraSettings(BaseSettings):
  mongo: MongoSettings
  bigquery: BigQuerySettings
  redis: RedisSettings
  kafka: KafkaSettings