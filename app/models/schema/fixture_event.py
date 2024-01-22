from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse

class ResponseData(BaseModel):
    ...

class Parameters(BaseModel):
    season: Optional[int] = None
    league_id: Optional[int] = None
    fixture: int

class FixtureEventResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
