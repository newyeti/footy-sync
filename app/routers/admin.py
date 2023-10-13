from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from typing import Any
from dependency_injector.wiring import inject, Provide

from app.dependencies.containers import Container
from app.dependencies.services import Service
from app.dependencies.service_models import ServiceException, Tags
from app.dependencies.constants import AppSettingsDependency
from app.dependencies.functions import isNotNull
from app.dependencies.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
            tags=["teams"]
        )

@router.get("/", 
            tags=[Tags.admin], 
            name="Health check",
            status_code=status.HTTP_200_OK)
async def health(settings: AppSettingsDependency) -> Any:
    return {"status": f"{settings.app_name} service is running."}


@router.get("/settings", 
            tags=[Tags.admin], 
            name="App Settings",
            status_code=status.HTTP_200_OK)
async def settings(settings: AppSettingsDependency) -> Any:
    return {
        "mongo": isNotNull(settings.mongo),
        "redis": isNotNull(settings.redis),
        "bigquery": isNotNull(settings.bigquery),
        "rapid_api_keys": isNotNull(settings.rapid_api)
    }

@router.get("/connect/test/redis", 
            tags=[Tags.admin], 
            name="Connection test for Redis",
            status_code=status.HTTP_200_OK)
@inject
async def test_dependency(service: Service = Depends(Provide[Container.service])):
    value = await service.redis_conn_test()
    return {"connection": value}