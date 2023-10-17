from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.settings.base import MongoSetting
from app.db.errors import ConnectionError

class MongoClient:
    
    db: AsyncIOMotorDatabase = None
    
    def __init__(self, uri: str, settings: MongoSetting):
        self.client = AsyncIOMotorClient(settings.get_uri(), ssl=True, tlsAllowInvalidCertificates=True)
        self.db = self.client.get_database(settings.db)
        
    
    async def is_connected(self):
        try:
            return await self.client.server_info()
        except Exception as e:
            raise ConnectionError(str(e))
        
        
    def close(self):
        try:
            self.client.close()
        except Exception as e:
            raise ConnectionError(str(e))