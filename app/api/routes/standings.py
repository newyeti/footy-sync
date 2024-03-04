from typing import Any
from fastapi import APIRouter, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject, Provide

from app.api.routes.common import CommonsPathDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.standings_service import StandingsService

from app.core.auth.utils import VerifyToken

router = APIRouter()
token_verifier = VerifyToken()

@router.post("/standings/{season}/{league_id}", 
            name="standings:sync",
            summary = "Synchornize standings data",
            description = "Retrive standings data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_standings(params: CommonsPathDependency,
                         auth_result: str = Security(token_verifier.verify),
                     standings_service: StandingsService = Depends(Provide[Container.standings_service])) -> Any:
    await standings_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="standings",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

