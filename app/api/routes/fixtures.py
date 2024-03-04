from typing import Any
import datetime
from dateutil import parser
from fastapi import APIRouter, status, Depends, Security
from fastapi.encoders import jsonable_encoder
from loguru import logger
from dependency_injector.wiring import inject

from app.api.routes.common import CommonsPathDependency
from app.models.schema.response import ApiResponse, ApiResponseStatus

from app.api.dependencies.container import Container
from app.services.fixtures_service import FixtureService
from app.services.fixture_lineup_service import FixtureLineupService
from app.services.fixture_events_service import FixtureEventsService
from app.services.fixture_player_stats_service import FixturePlayerStatsService
from app.services.fixture_template_service import FixtureTemplateService
from dependency_injector.wiring import inject, Provide
from app.api.errors.service_error import ServiceException
from app.core.auth.utils import VerifyToken

router = APIRouter()
token_verifier = VerifyToken()

@router.post("/fixtures/{season}/{league_id}", 
            name="fixtures:sync_fixtures",
            summary = "Synchornize fixture data",
            description = "Retrive fixtures data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_fixtures(params: CommonsPathDependency,
                        auth_result: str = Security(token_verifier.verify),
                        fixture_id: int | None = None,
                        fixture_service: FixtureService = Depends(Provide[Container.fixture_service])) -> Any:
    await fixture_service.execute(season=params.season, league_id=params.league_id, fixture_id=fixture_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            fixture_id=fixture_id,
                            service="fixtures",
                            status= ApiResponseStatus.success)   
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/fixtures/lineup/{season}/{league_id}/{fixture_id}",
            name="fixtures:sync_fixture_lineup",
            summary = "Synchornize fixture lineup data",
            description = "Retrive fixtures data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_fixuture_lineup(params: CommonsPathDependency, 
                               fixture_id: int,
                               fixture_lineup_service: FixtureLineupService = Depends(Provide[Container.fixture_lineup_service]),
                               auth_result: str = Security(token_verifier.verify)
                               ) -> Any:
    await fixture_lineup_service.execute(season=params.season, 
                                          league_id=params.league_id, 
                                          fixture_id=fixture_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            fixture_id=fixture_id,
                            service="fixtures_lineups",
                            status= ApiResponseStatus.success)
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/fixtures/events/{season}/{league_id}/{fixture_id}",
            name="fixtures:sync_fixuture_events",
            summary = "Synchornize fixture events data",
            description = "Retrive fixture events data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_fixuture_events(params: CommonsPathDependency, fixture_id: int,
                               fixture_events_service: FixtureEventsService = Depends(Provide[Container.fixture_events_service]),
                               auth_result: str = Security(token_verifier.verify)
                               ) -> Any:
    await fixture_events_service.execute(season=params.season, 
                                          league_id=params.league_id, 
                                          fixture_id=fixture_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            fixture_id=fixture_id,
                            service="fixture_events",
                            status= ApiResponseStatus.success)
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/fixtures/stats/{season}/{league_id}/{fixture_id}",
            name="fixtures:sync_fixuture_player_stats",
            summary = "Synchornize fixture player statistics data",
            description = "Retrive fixture player statistics data from API and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_fixuture_player_stats(params: CommonsPathDependency, fixture_id: int,
                               fixture_player_stats_service: FixturePlayerStatsService = Depends(Provide[Container.fixture_player_stats_service]),
                               auth_result: str = Security(token_verifier.verify)
                               ) -> Any:
    await fixture_player_stats_service.execute(season=params.season, 
                                          league_id=params.league_id, 
                                          fixture_id=fixture_id)
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            fixture_id=fixture_id,
                            service="fixture_player_stats",
                            status= ApiResponseStatus.success)
    return jsonable_encoder(service_response, exclude_none=True)

@router.post("/fixtures/stat/{season}/{league_id}",
            name="fixtures:sync_fixuture_template",
            summary = "Synchornize fixture, lineup, events and player stats",
            description = "Retrive fixture by date and retrieve fixture, lineup, events  and player stats from api and updates database",
            status_code=status.HTTP_200_OK,
            response_model=ApiResponse,
            response_model_exclude_defaults=True)
@inject
async def sync_fixtures_by_date(params: CommonsPathDependency, 
                                from_date: str | None = None,
                                to_date: str | None = None,
                                fixture_template_service: FixtureTemplateService = Depends(Provide[Container.fixture_template_service]),
                                auth_result: str = Security(token_verifier.verify)) -> Any:
    date_format = "%Y-%m-%d"
    
    def validate_date(date: str) -> datetime.date:
        try:
            return datetime.date.fromisoformat(date)
        except ValueError as e:
            raise ServiceException(name= "fixtures", message="Invalid date. Date should be in YYYY-MM-DD format.")

    if (from_date and not to_date) or (not from_date and to_date):
        raise ServiceException(name= "fixtures", message="From date and To date must be provided together.")

    if from_date:
        fdate = validate_date(date=from_date)   
    else:
        fdate = datetime.datetime.now().date()
        
    if to_date:
        tdate = validate_date(date=to_date) 
    else:
        tdate = (datetime.datetime.now() + datetime.timedelta(1)).date()
        
    if fdate > tdate:
        raise ServiceException(name="fixtures", message="From date cannot be less than To date.")
    
    # Increment to date by 1 to find document with event date between dates
    tdate = datetime.date(tdate.year, tdate.month, tdate.day+1)
    
    await fixture_template_service.update_by_date(
        season=params.season,
        league_id=params.league_id,
        fromDate=fdate.strftime(date_format),
        toDate=tdate.strftime(date_format)
    )
    
    service_response = ApiResponse(season=params.season, 
                            league_id=params.league_id,
                            service="fixtures_by_date",
                            status= ApiResponseStatus.success)
    return jsonable_encoder(service_response, exclude_none=True)

