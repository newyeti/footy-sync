
from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse

class Color(BaseModel):
    primary: Optional[str| None] = None
    number: Optional[str| None] = None
    border: Optional[str| None] = None

class TeamColor(BaseModel):
    player: Optional[Color | None] = None
    goalkeeper: Optional[Color | None] = None 

class Team(BaseModel):
    id: int
    name: str
    logo: str
    colors: Optional[TeamColor | None] = None

class Coach(BaseModel):
    id: int
    name: str
    photo: str

class Player(BaseModel):
    id: int
    name: str
    number: int
    pos: str
    grid: Optional[str | None] = None

class Players(BaseModel):
    player: Player

class ResponseData(BaseModel):
    team: Team 
    coach: Optional[Coach | None] = None
    formation: Optional[str | None] = None
    startXI: Optional[list[Players | None]] = None 
    substitutes: Optional[list[Players| None]] = None

class Parameters(BaseModel):
    season: Optional[int] = None
    league_id: Optional[int] = None
    fixture: int

class FixtureLineUpResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
