from typing import Annotated
from fastapi import Depends
from ..config import Settings
from ..dependencies.functions import get_settings
from ..internal.services.models import CommonPathParams

AppSettingsDependency = Annotated[Settings, Depends(get_settings)]
CommonsPathDependency = Annotated[CommonPathParams, Depends()]

rapid_api_hostname = "api-football-v1.p.rapidapi.com"
rapid_api_key = "U4y3LniAIdmsh1SryySGibO7k8ELp1syFPvjsnpHOQNWAvpJAk"
headers = {
            'X-RapidAPI-Key': "U4y3LniAIdmsh1SryySGibO7k8ELp1syFPvjsnpHOQNWAvpJAk",
            'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
        }
