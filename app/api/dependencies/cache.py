import json

from aioredis import Redis

class CacheService:
    
    def __init__(self, provider: Redis) -> None:
        self.__provider = provider


    async def get(self, key):
        return await self.__provider.get(str(key)) 


    async def set(self, key, value, exp=None):
        return await self.__provider.set(str(key), value, exp)


    async def delete(self, key):
        return await self.__provider.delete(str(key))


    async def get_all(self):
        keys = await self.__provider.keys("*")
        return [json.loads(await self.__provider.get(key)) for key in keys]
    
    
    def get_key(self, key: str, prefix: str = "", suffix: str = ""):
        if prefix is None:
            prefix = ""
        elif prefix != "":
            prefix = f"{prefix}::"
        
        if suffix is None:
            suffix = ""
        elif suffix != "":
            suffix = f"::{suffix}"
        
        return f"{prefix}{key}{suffix}"