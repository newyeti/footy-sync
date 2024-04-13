from loguru import logger
from datetime import datetime, timedelta
from app.api.dependencies.linked_list import LinkedList
from app.api.dependencies.cache import CacheService
from app.core.settings.base import RapidApiSetting

class ApiKeyData:
    key: str
    count: int
    
    def __init__(self, key: str, count: int) -> None:
        self.key = key
        self.count = count

class ApiKeyService:
    keys: LinkedList[ApiKeyData]
    daily_api_access_count: int
    key_index: int = 0
    
    def __init__(self,
                 cache_service: CacheService,
                 settings: RapidApiSetting) -> None:
        self.cache_service = cache_service
        self.api_keys = settings.api_keys
        self.daily_limit = settings.daily_limit
        self.cache_key = settings.cache_key
        self.cache_key_expiry_in_days = settings.cache_key_expiry_in_days
        self.initializeKeys()
    
    def initializeKeys(self):
        self.keys = LinkedList[ApiKeyData]()
        for key in self.api_keys:
            self.keys.append(ApiKeyData(key, 0))
        self.current_key = self.keys.head
        
    def get_api_cache_key(self) -> str:
        return self.cache_service.get_key(key=self.cache_key,
                                            suffix=datetime.now().date())
        
    async def get_cached_count(self) -> int:
        cache_key = self.get_api_cache_key()
        api_calls = await self.cache_service.get(cache_key)
                
        if api_calls:
            return int(api_calls)
        else:
            self.initializeKeys()
            return 0
    
    async def get(self) -> str:
        self.daily_api_access_count = await self.get_cached_count()
        logger.info(f'''Total Daily API calls={self.daily_api_access_count}
                        Daily Limit per Key={self.daily_limit}
                        Total Daily Limit={self.daily_limit * len(self.api_keys)}
                    ''')
        
        count_per_key = self.daily_api_access_count % self.daily_limit
        
        if self.daily_api_access_count == 0:
            return self.current_key.data.key
        if count_per_key > 0 and count_per_key < self.daily_limit:
            return self.current_key.data.key
        
        index: int = int(self.daily_api_access_count / self.daily_limit)
        for i in range(0, index-self.key_index):
            if self.current_key:
                self.key_index += 1
                self.current_key.data.count = self.daily_limit
                self.current_key = self.current_key.next
        
        if self.current_key:
            self.current_key.data.count = self.daily_api_access_count % self.daily_limit
            return self.current_key.data.key
        
        return None
    
    async def update_apiaccess_cache_count(self):
        await self.cache_service.set(key=self.get_api_cache_key(), 
                                    value= str(self.daily_api_access_count + 1),
                                    exp=timedelta(days=self.cache_key_expiry_in_days))
    