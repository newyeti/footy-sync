from typing import Any
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject

from app.api.routes.common import CommonsPathDependency, AppSettingsDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.teams import TeamService
from dependency_injector.wiring import inject, Provide

router = APIRouter()


@router.post("/teams/{season}/{league_id}", 
            name="teams:sync_teams",
            summary = "Synchornize teams data",
            description = "Retrive teams data from API and updates database",
            status_code=status.HTTP_200_OK)
@inject
async def sync_teams(params: CommonsPathDependency,
                     app_settings: AppSettingsDependency,
                     team_service: TeamService = Depends(Provide[Container.team_service])) -> Any:
    logger.debug(params)
    await team_service.sync(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=2023, 
                            league_id=39,
                            service="teams",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)
