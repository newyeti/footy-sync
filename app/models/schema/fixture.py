from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse

class ResponseData(BaseModel):
    ...

class Parameters(BaseModel):
    league: Optional[int]
    season: Optional[int]
    fixture_id: Optional[int]
    date: Optional[str]

class FixtureResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]