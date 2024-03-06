from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse

class Periods(BaseModel):
    first: Optional[int] = None
    second: Optional[int] = None

class Venue(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    city: Optional[str] = None

class Status(BaseModel):
    long: Optional[str] = None
    short: Optional[str] = None
    elapsed: Optional[int] = None
    
class Fixture(BaseModel):
    id: int
    referee: Optional[str] = None
    timezone: Optional[str] = None
    date: Optional[str] = None
    timestamp: Optional[int] = None
    periods: Optional[Periods] = None
    venue: Optional[Venue] = None
    status: Optional[Status] = None

class League(BaseModel):
    id: int
    name: str
    country: str
    logo: Optional[str] = None
    flag: Optional[str] = None
    season: int
    round: str

class Team(BaseModel):
    id: int 
    name: str 
    logo: Optional[str] = None
    winner: Optional[bool] = None

class Teams(BaseModel):
    home: Team
    away: Team   
    
class Goals(BaseModel):
    home: Optional[int] = None
    away: Optional[int] = None

class Score(BaseModel):
    halftime: Goals
    fulltime: Goals
    extratime: Optional[Goals] = None
    penalty: Optional[Goals] = None
    
class ResponseData(BaseModel):
    fixture: Fixture
    league: League
    teams: Teams
    goals: Goals
    score: Score

class Parameters(BaseModel):
    league: Optional[int | None] = None
    season: Optional[int | None] = None
    fixture_id: Optional[int | None] = None
    date: Optional[str | None] = None

class FixtureResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]