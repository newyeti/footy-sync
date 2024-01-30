from typing import Any
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject

from app.api.routes.common import CommonsPathDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.top_scorers_service import TopScorersService
from dependency_injector.wiring import inject, Provide

router = APIRouter()

@router.post("/players/topscorers/{season}/{league_id}", 
            name="topscorers:sync",
            summary = "Synchornize top scorers data",
            description = "Retrive top scorers data from API and updates database",
            status_code=status.HTTP_200_OK)
@inject
async def sync_standings(params: CommonsPathDependency,
                     top_scorers_service: TopScorersService = Depends(Provide[Container.top_scorers_service])) -> Any:
    await top_scorers_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="top_scorers",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

