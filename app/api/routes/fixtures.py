from typing import Any
from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject

from app.api.routes.common import CommonsPathDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.fixture_service import FixtureService
from app.services.fixture_lineup_service import FixtureLineupService
from dependency_injector.wiring import inject, Provide

router = APIRouter()

@router.post("/fixtures/{season}/{league_id}", 
            name="fixtures:sync_fixtures",
            summary = "Synchornize fixture data",
            description = "Retrive fixtures data from API and updates database",
            status_code=status.HTTP_200_OK)
@inject
async def sync_fixtures(params: CommonsPathDependency,
                     fixture_service: FixtureService = Depends(Provide[Container.fixture_service])) -> Any:
    await fixture_service.execute(season=params.season, league_id=params.league_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="fixtures",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/fixtures/lineup/{season}/{league_id}/{fixture_id}",
            name="fixtures:sync_fixture_lineup",
            summary = "Synchornize fixture data",
            description = "Retrive fixtures data from API and updates database",
            status_code=status.HTTP_200_OK)
@inject
async def sync_fixuture_lineup(params: CommonsPathDependency, fixture_id: int,
                               fixture_lineup_service: FixtureLineupService = Depends(Provide[Container.fixture_lineup_service])
                               ) -> Any:
    await fixture_lineup_service.execute(season=params.season, 
                                          league_id=params.league_id, 
                                          fixture_id=fixture_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="fixtures_lineups",
                            status= ApiResponseStatus.success)
    return jsonable_encoder(service_response, exclude_none=True)
