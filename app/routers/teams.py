from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from dependency_injector.wiring import inject, Provide
from typing import Any

from ..internal.services.models import ServiceResponse, Tags, ServiceStatus
from ..internal.services.services import TeamService
from ..dependencies.logger import get_logger
from ..dependencies.exceptions import ServiceException
from ..dependencies.containers import Container
from ..dependencies.constants import CommonsPathDependency, AppSettingsDependency

logger = get_logger(__name__)

router = APIRouter(
            tags=["teams"]
        )

@router.post("/teams/{season}/{league_id}",
          status_code=status.HTTP_200_OK,
          summary = "Synchornize teams data",
          description = "Retrive teams data from API and updates database",
          tags=[Tags.teams],
          response_model=ServiceResponse)
@inject
async def sync_teams(path_params: CommonsPathDependency,
                     settings: AppSettingsDependency,
                        team_service: TeamService = Depends(Provide[Container.team_service]),
                        ) -> Any:
    
    response = await team_service.upsert(path_params=path_params, settings=settings)
    
    logger.debug(response)
    
    if response.status_code == status.HTTP_200_OK:
        response = ServiceResponse(season=2023, 
                                league_id=39,
                                service="teams",
                                status= ServiceStatus.success)   
        return jsonable_encoder(response)
    else:
        raise ServiceException(name="teams", message = response.response_data)

            
    