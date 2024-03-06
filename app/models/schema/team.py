from pydantic import BaseModel
from typing import Optional, Any
from app.models.schema.rapid_api_response import RapidApiResponse

class Team(BaseModel):
    id: int
    name: str
    code: str
    country: Optional[str] = None
    founded: Optional[int] = None
    national: Optional[bool] = None
    logo: Optional[str]


class Venue(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    capacity: Optional[int] = None
    surface: Optional[str] = None
    image: Optional[str] =  None


class ResponseData(BaseModel):
    team: Team
    venue: Venue

class Parameters(BaseModel):
    league: int
    season: int

class TeamInRapidApiResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
    





