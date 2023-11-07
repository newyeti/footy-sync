import aiohttp
import asyncio

from functools import lru_cache
from typing import Any
from loguru import logger
from fastapi import status
from datetime import datetime, timedelta

from app.core.settings.base import RapidApiSetting
from app.models.schema.response import HttpResponse
from app.services.base_service import ApiService
from app.api.dependencies.cache import CacheService
from app.api.errors.service_error import RapidApiException


@lru_cache()
def get_api_key(keys: str):
    api_keys = keys.split(",")
    return api_keys[0]


def get_request_header(settings: RapidApiSetting):
    return {
            'X-RapidAPI-Key': get_api_key(settings.api_keys),
            'X-RapidAPI-Host': settings.api_hostname
        }


async def get_request(session: aiohttp.ClientSession, url: str,
                      **kwargs: Any) -> HttpResponse:
    try:
        async with session.get(url=url, **kwargs, ssl=False) as response:
            status_code = response.status
            headers = response.headers
            response_content_type = headers.get('Content-Type')
            
            if 'json' in response_content_type:
                response_data = await response.json()
            else:
                response_data = await response.text()
            return HttpResponse(headers=headers, status_code=status_code, response_data=response_data)
    except aiohttp.ClientError as e:
        return {"error": f"Error getting data from {url}: {e}"}
    

async def post_request(session: aiohttp.ClientSession, 
                       url: str, 
                       auth: aiohttp.BasicAuth, 
                       data: dict):
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        async with session.post(url=url,
                                data=data,
                                headers=headers,
                                auth=auth, 
                                ssl=False) as response:
            response_content_type = response.content_type
            status_code = response.status
            
            if 'json' in response_content_type:
                response_data = await response.json()
            else:
                response_data = await response.text()
            logger.info(f"status={response.status}, message={response_data}")
            return HttpResponse(headers=headers, status_code=status_code, response_data=response_data)
        
    except aiohttp.ClientError as e:
        return {"error": f"Error posting data to {url}: {e}"}
    


class RapidApiService(ApiService):
    
    def __init__(self, 
                 settings: RapidApiSetting, 
                 cache_service: CacheService) -> None:
        self.settings = settings
        self.cache_service = cache_service


    async def fetch_from_api(self,
                             endpoint: str,
                             season: int, 
                             league_id: int) -> HttpResponse:
        cache_key = self.cache_service.get_key(key=self.settings.cache_key,
                                                suffix=datetime.now().date())
        api_calls = await self.cache_service.get(cache_key)
        
        if api_calls and int(api_calls) > self.settings.daily_limit:
            raise RapidApiException(name="teams", message = "Daily limit reached for Rapid API Key.")
        
        
        url = f"https://{self.settings.api_hostname}{endpoint}"
        headers = get_request_header(settings=self.settings)
        params = {
            "season": season,
            "league": league_id
        }

        logger.debug(f"calling endpoint={url}")

        async with aiohttp.ClientSession() as session:
            try:
                result = await asyncio.gather(get_request(session=session,
                                url=url, params=params, headers=headers))
                
                
                if api_calls is None:
                    api_calls = "0"
                
                await self.cache_service.set(key=cache_key, 
                                             value= int(api_calls) + 1,
                                             exp=timedelta(days=self.settings.cache_key_expiry_in_days))
                
                api_response = result[0]
                if api_response.status_code == status.HTTP_200_OK:
                    return api_response
                else:
                    logger.error(f"rapidAPI response: url={url}, error={api_response.response_data['message']}")
                    raise RapidApiException(name="teams",
                                            api_url=url,
                                            message = api_response.response_data['message'])
                
            except aiohttp.ClientError as e:
                raise RapidApiException(name="teams", message = str(e))