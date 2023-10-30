from typing import Any
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


class AppException(Exception):
    def __init__(self, message: Any):
        self.message = message

async def app_error_handler(_: Request, exec: AppException) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = jsonable_encoder(exec, 
                                   exclude_none=True, 
                                   exclude_unset=True,
                                   exclude_defaults=True),
    )
