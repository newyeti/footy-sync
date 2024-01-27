from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import RapidApiResponse

class Team(BaseModel):
    id : int
    name: str
    logo: Optional[str] = Field(default=None)

class Goal(BaseModel):
    for_: Optional[int] = Field(default=0, alias="for")
    against: Optional[int] = Field(default=0)

class Stat(BaseModel):
    played: Optional[int] = Field(default=0)
    win: Optional[int] = Field(default=0)
    draw: Optional[int] = Field(default=0)
    lose: Optional[int] = Field(default=0)
    goals: Optional[Goal] = Field(default=None)

class TeamStandings(BaseModel):
    rank: int
    team: Team
    points: int
    goalsDiff: Optional[int] = Field(default=None)
    group: str
    form: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    all: Stat 
    home: Stat
    away: Stat
    update: Optional[str] = Field(default=None)
    
class League(BaseModel):
    id: int 
    name: str
    country: str
    logo: Optional[str]
    flag: Optional[str]
    season: int
    standings: list[list[TeamStandings]]

class ResponseData(BaseModel):
    league: League

class Parameters(BaseModel):
    season: Optional[int] = None
    league_id: Optional[int] = None

class StandingsResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
