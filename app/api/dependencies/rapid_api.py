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
from app.api.dependencies.api_key import ApiKeyService


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
                 cache_service: CacheService,
                 apikey_service: ApiKeyService) -> None:
        self.settings = settings
        self.cache_service = cache_service
        self.apikey_service = apikey_service

    def __get_request_header(self, api_hostname: str, api_key: str):
        return {
                'X-RapidAPI-Key': api_key,
                'X-RapidAPI-Host': api_hostname
            }
    
    async def fetch_from_api(self,
                             endpoint: str,
                             params: dict) -> HttpResponse:
        api_key = await self.apikey_service.get()
        
        logger.info(f'Got API key={api_key}')
        
        if api_key is None:
            raise RapidApiException(name="teams", message = "Daily limit reached for Rapid API Key.")
        
        url = f"https://{self.settings.api_hostname}{endpoint}"
        headers = self.__get_request_header(api_hostname=self.settings.api_hostname,
                                          api_key=api_key)
        logger.info(f"calling endpoint={url}")

        async with aiohttp.ClientSession() as session:
            try:
                result = await asyncio.gather(get_request(session=session,
                                url=url, params=params, headers=headers))
                 
                await self.apikey_service.update_apiaccess_cache_count()
                
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