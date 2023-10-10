from pydantic_settings import BaseSettings

class Database(BaseSettings):
    host: str
    port: str
    username: str
    password: str

class Settings(BaseSettings):
    app_name: str = "Footy-Sync"
    mongo_db: Database

