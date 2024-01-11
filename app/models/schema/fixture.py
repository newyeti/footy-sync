from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse

class Periods(BaseModel):
    first: Optional[int] = None
    second: Optional[int] = None

class Venue(BaseModel):
    id: int
    name: str
    city: str

class Status(BaseModel):
    long: str
    short: str
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
    logo: str
    flag: Optional[str] = None
    season: int
    round: str

class Team(BaseModel):
    id: int 
    name: str 
    logo: str
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
    league: Optional[int]
    season: Optional[int]
    fixture_id: Optional[int] = None
    date: Optional[str] = None

class FixtureResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]