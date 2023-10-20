from typing import Annotated
from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from app.core.settings.app import AppSettings
from app.core.config import get_app_settings
from app.models.schema.api import CommonPathParams
from app.api.dependencies.container import Container
from app.services.teams import TeamService


AppSettingsDependency = Annotated[AppSettings, Depends(get_app_settings)]
CommonsPathDependency = Annotated[CommonPathParams, Depends()]

