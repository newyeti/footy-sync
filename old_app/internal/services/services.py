import json
import aiohttp
import asyncio
import json

from fastapi import params, status
from aioredis import Redis
from app.dependencies.logger import get_logger
from app.dependencies.constants import CommonsPathDependency, AppSettingsDependency
from app.dependencies.functions import get_request_header, get_request
from app.dependencies.exceptions import ServiceException
from app.internal.db.repositorys import TeamRepository

logger = get_logger(__name__)


class CacheService:
    def __init__(self, provider: Redis) -> None:
        self.__provider = provider

    async def get(self, key):
        value = await self.__provider.get(str(key))
        return json.loads(value) if value else None

    async def set(self, key, value, exp=None):
        return await self.__provider.set(str(key), value, exp)

    async def delete(self, key):
        return await self.__provider.delete(str(key))

    async def get_all(self):
        keys = await self.__provider.keys("*")
        return [json.loads(await self.__provider.get(key)) for key in keys]


class ApiService:
    def __init__(self):
        ...

    async def fetch(self, 
                    endpoint: str, 
                    path_params: CommonsPathDependency, 
                    settings: AppSettingsDependency):
        
        url = f"https://{settings.rapid_api.api_hostname}{endpoint}"
        headers = get_request_header(settings=settings)
        params = {
            "season": path_params.season,
            "league": path_params.league_id
        }
        
        logger.debug(f"calling endpoint={url}")
        
        async with aiohttp.ClientSession() as session:
            try:
                result = await asyncio.gather(get_request(session=session,
                                url=url, params=params, headers=headers))
                
                logger.debug(f"rapid api response= {result[0]}") 
                
                api_response = result[0]
                if api_response.status_code == status.HTTP_200_OK:
                    return api_response
                else:
                    logger.error(f"rapidAPI response: url={url}, error={api_response.response_data['message']}")
                    raise ServiceException(name="teams",
                                           api_url=url,
                                           message = api_response.response_data['message'])
                
            except aiohttp.ClientError as e:
                raise ServiceException(name="teams", message = str(e))
    

class TeamService:
    def __init__(self, 
                 api_service: ApiService,
                 cache_service: CacheService,
                 repository: TeamRepository) -> None:
        self._api_service = api_service
        self._cache_service = cache_service
        self._repository = repository
    
    
    async def upsert(self, path_params: CommonsPathDependency, settings: AppSettingsDependency):
        return await self._api_service.fetch("/v3/teams", path_params=path_params, settings=settings)
    


