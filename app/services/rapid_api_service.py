from typing import Any

from app.services.interface import ApiService
from app.api.dependencies.cache import CacheService


class RapidApiService(ApiService):
    def __init__(self, cache_service: CacheService) -> None:
        self.cache_service = cache_service

    async def fetch_from_api(self,
                             settings: Any, 
                             uri,
                             season: int, 
                             league_id: int) -> Any:
        ...

#     async def fetch(self, 
#                     endpoint: str, 
#                     path_params: CommonsPathDependency, 
#                     settings: AppSettingsDependency):
        
#         url = f"https://{settings.rapid_api.api_hostname}{endpoint}"
#         headers = get_request_header(settings=settings)
#         params = {
#             "season": path_params.season,
#             "league": path_params.league_id
#         }
        
#         logger.debug(f"calling endpoint={url}")
        
#         async with aiohttp.ClientSession() as session:
#             try:
#                 result = await asyncio.gather(get_request(session=session,
#                                 url=url, params=params, headers=headers))
                
#                 logger.debug(f"rapid api response= {result[0]}") 
                
#                 api_response = result[0]
#                 if api_response.status_code == status.HTTP_200_OK:
#                     return api_response
#                 else:
#                     logger.error(f"rapidAPI response: url={url}, error={api_response.response_data['message']}")
#                     raise ServiceException(name="teams",
#                                            api_url=url,
#                                            message = api_response.response_data['message'])
                
#             except aiohttp.ClientError as e:
#                 raise ServiceException(name="teams", message = str(e))