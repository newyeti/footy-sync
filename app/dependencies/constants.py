from typing import Annotated
from fastapi import Depends
from ..config import Settings
from ..dependencies.functions import get_settings

AppSettings = Annotated[Settings, Depends(get_settings)]

rapid_api_hostname = "api-football-v1.p.rapidapi.com"
rapid_api_key = "U4y3LniAIdmsh1SryySGibO7k8ELp1syFPvjsnpHOQNWAvpJAk"
headers = {
            'X-RapidAPI-Key': rapid_api_key,
            'X-RapidAPI-Host': rapid_api_hostname
        }
