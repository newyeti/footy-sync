from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from typing import Any

import logging
import aiohttp
import asyncio
from ..dependencies.service_models import ServiceResponse, Tags, ServiceStatus, ServiceException
from ..dependencies.functions import get_request, get_request_header
from ..dependencies.constants import CommonsPathDependency, AppSettingsDependency

logger = logging.getLogger(__name__)

router = APIRouter(
            tags=["teams"]
        )

@router.post("/teams/{season}/{league_id}",
          status_code=status.HTTP_200_OK,
          summary = "Synchornize teams data",
          description = "Retrive teams data from API and updates database",
          tags=[Tags.teams],
          response_model=ServiceResponse)
async def sync_teams(path_params: CommonsPathDependency,
                     settings: AppSettingsDependency) -> Any:
    
    logger.debug(f"calling endpoint=/teams/{path_params.season}/{path_params.league_id}")

    url = f"https://{settings.rapid_api.api_hostname}/v3/teams"
    headers = get_request_header(settings=settings)
    params = {
        "season": path_params.season,
        "league": path_params.league_id
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            result = await asyncio.gather(get_request(session=session,
                            url=url, params=params, headers=headers))
            
            logger.info(result[0]) 
            
            api_response = result[0]
            if api_response.status_code == status.HTTP_200_OK:
                response = ServiceResponse(season=path_params.season, 
                                       league_id=path_params.league_id,
                                       service="teams",
                                       status= ServiceStatus.success)   
                return jsonable_encoder(response)
            else:
                raise ServiceException(name="teams", message = api_response.response_data)
            
        except aiohttp.ClientError as e:
            raise ServiceException(name="teams", message = str(e))
            
    