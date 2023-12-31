from pydantic import BaseModel
from typing import Optional, Any
from app.models.schema.rapid_api_response import RapidApiResponse

class Team(BaseModel):
    id: int
    name: str
    code: str
    country: str
    founded: int
    national: bool
    logo: str


class Venue(BaseModel):
    id: int
    name: str
    address: str
    city: str
    capacity: int
    surface: str
    image: str


class ResponseData(BaseModel):
    team: Team
    venue: Venue

class Parameters(BaseModel):
    league: int
    season: int
    
class Paging(BaseModel):
    current: int
    total: int

class TeamInRapidApiResponse(BaseModel):
    get: str
    parameters: Parameters
    errors: Optional[Any]
    results: int
    paging: Paging
    response: list[ResponseData]
    





