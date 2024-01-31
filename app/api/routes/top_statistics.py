from typing import Any
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject

from app.api.routes.common import CommonsPathDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.top_players_service import (
    TopScorersService,
    TopAssistsService,
    TopRedCardsService,
    TopYellowCardsService,
)
from dependency_injector.wiring import inject, Provide

router = APIRouter()

@router.post("/players/topscorers/{season}/{league_id}", 
            name="topscorers:sync",
            summary = "Synchornize top scorering players data",
            description = "Retrive top scorers players data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_standings(params: CommonsPathDependency,
                     top_scorers_service: TopScorersService = Depends(Provide[Container.top_scorers_service])) -> Any:
    await top_scorers_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="top_scorers",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/players/topassists/{season}/{league_id}", 
            name="topassists:sync",
            summary = "Synchornize top assisting players data",
            description = "Retrive top assisting players data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_standings(params: CommonsPathDependency,
                     top_assists_service: TopAssistsService = Depends(Provide[Container.top_assists_service])) -> Any:
    await top_assists_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="top_assists",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/players/topredcards/{season}/{league_id}", 
            name="topreadcards:sync",
            summary = "Synchornize top red carded players data",
            description = "Retrive top red carded players data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_standings(params: CommonsPathDependency,
                     top_redcards_service: TopRedCardsService = Depends(Provide[Container.top_redcards_service])) -> Any:
    await top_redcards_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="top_red_cards",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/players/topyellowcards/{season}/{league_id}", 
            name="topyellowcards:sync",
            summary = "Synchornize top yellow carded players data",
            description = "Retrive top yellow carded players data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_standings(params: CommonsPathDependency,
                     top_yellowcards_service: TopYellowCardsService = Depends(Provide[Container.top_yellowcards_service])) -> Any:
    await top_yellowcards_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="top_yellow_cards",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)