from pydantic import BaseModel
from typing import Optional

from app.models.common import RapidApiResponse


class Time(BaseModel):
    elapsed: int
    extra: Optional[int] = None
    
class Team(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    
class Player(BaseModel):
    id: int
    name: str
    
class Assist(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class ResponseData(BaseModel):
    time: Time
    team: Team
    player: Player
    assist: Optional[Assist] = None
    type: str
    detail: str
    comments: Optional[str] = None

class Parameters(BaseModel):
    season: Optional[int] = None
    league_id: Optional[int] = None
    fixture: int

class FixtureEventResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
