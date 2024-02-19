from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import RapidApiResponse

class Shots(BaseModel):
    total: Optional[int] = Field(default=0)
    on: Optional[int] = Field(default=0)

class Goals(BaseModel):
    total: Optional[int] = Field(default=0)
    conceded: Optional[int] = Field(default=0)
    assists: Optional[int] = Field(default=0)
    saves: Optional[int] = Field(default=0)

class Passes(BaseModel):
    total: Optional[int] = Field(default=0)
    key: Optional[int] = Field(default=0)
    accuracy: Optional[int] = Field(default=0)

class Tackles(BaseModel):
    total: Optional[int]  = Field(default=0)
    blocks: Optional[int] = Field(default=0)
    interceptions: Optional[int] = Field(default=0)

class Duels(BaseModel):
    total: Optional[int] = Field(default=0)
    won: Optional[int] = Field(default=0)

class Dribbles(BaseModel):
    attempts: Optional[int] = Field(default=0)
    success: Optional[int] = Field(default=0)
    past: Optional[int] = Field(default=0)

class Fouls(BaseModel):
    drawn: Optional[int] = Field(default=0)
    committed: Optional[int] = Field(default=0)

class Cards(BaseModel):
    yellow: Optional[int] = Field(default=0)
    red: Optional[int] = Field(default=0)

class Penalty(BaseModel):
    won: Optional[int] = Field(default=0)
    committed: Optional[int] = Field(default=0)
    success: Optional[int] = Field(default=0)
    saved: Optional[int] = Field(default=0)

class Games(BaseModel):
    minutes: Optional[int] = Field(default=0)
    number: Optional[int] = Field(default=0)
    position: Optional[str] = Field(default=0)
    rating: Optional[float] = Field(default=0)
    captain: Optional[bool] = Field(default= False)
    substitute: Optional[bool] = Field(default= False)

class Statistics(BaseModel):
    games: Games
    offsides: Optional[int]
    shots: Shots
    goals: Goals
    passes: Passes
    tackles: Tackles
    duels: Duels
    dribbles: Dribbles
    fouls: Fouls
    cards: Cards
    penalty: Penalty

class Player(BaseModel):
    id: int
    name: str
    photo: Optional[str]
    
class PlayerInfo(BaseModel):
    player: Player
    statistics: list[Statistics]

class Team(BaseModel):
    id: int
    name: str
    logo: Optional[str]
    update: Optional[str]
    
class ResponseData(BaseModel):
    team: Team
    players: list[PlayerInfo]

class Parameters(BaseModel):
    season: Optional[int] =None
    league_id: Optional[int] =None
    fixture: int

class FixtureStatResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
