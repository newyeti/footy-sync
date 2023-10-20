from pydantic import BaseModel
from typing import Optional, Any

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


class Response(BaseModel):
    team: Team
    venue: Venue


class Paging(BaseModel):
    current: int
    total: int

class Parameters(BaseModel):
    league: int
    season: int


class TeamInRapidApiResponse(BaseModel):
    get: str
    parameters: Parameters
    errors: Optional[Any]
    results: int
    paging: Paging
    response: Response





