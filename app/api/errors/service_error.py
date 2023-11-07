from typing import Any
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

        
class ServiceException(Exception):
    def __init__(self, name: str, api_url: str = "", message: Any = ""):
        self.name = name
        self.api_url = api_url
        self.message = message

class RapidApiException(ServiceException):
    ...
    

async def service_error_handler(_: Request, exec: ServiceException) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = jsonable_encoder(exec, 
                                   exclude_none=True, 
                                   exclude_unset=True,
                                   exclude_defaults=True),
    )
