from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import (
    RapidApiResponse, 
    Team,
    League
)

class Brith(BaseModel):
    date: Optional[str | None] = Field(default=None)
    place: Optional[str | None] = Field(default=None)
    country: Optional[str | None] = Field(default=None)

class Player(BaseModel):
    id: int 
    name: str
    firstname: str
    lastname: str
    age: Optional[int | None] = Field(default=0)
    birth: Optional[Brith]
    nationality: Optional[str | None] = Field(default=None)
    height: Optional[str | None] = Field(default=None)
    weight: Optional[str | None] = Field(default=None)
    injured: Optional[bool] = Field(default=False)
    photo: Optional[str | None] = Field(default=None)

class Games(BaseModel):
    appearences: int = Field(default=0)
    lineups: Optional[int | None] = Field(default=0)
    minutes: Optional[int | None] = Field(default=0)
    number: Optional[int] = Field(default=0)
    position: Optional[str | None] = Field(default=None)
    rating: Optional[str | None] = Field(default=None)
    captain: Optional[bool] = Field(default=False)

class Substitutes(BaseModel):
    in_: Optional[int | None] = Field(default=0, alias="in")
    out: Optional[int | None] = Field(default=0)
    bench: Optional[int | None] = Field(default=0)

class Shots(BaseModel):
    total: int = Field(default=0)
    on: int = Field(default=0)

class Goals(BaseModel):
    total: int = Field(default=0)
    conceded: Optional[int | None] = Field(default=0)
    assists: Optional[int | None] = Field(default=0)
    saves: Optional[int | None] = Field(default=0) 

class Passes(BaseModel):
    total: Optional[int | None] = Field(default=0)
    key: Optional[int | None] = Field(default=0)
    accuracy: Optional[int | None] = Field(default=0)

class Tackles(BaseModel):
    total: Optional[int | None] = Field(default=0)
    blocks: Optional[int | None] = Field(default=0)
    interceptions: Optional[int | None] = Field(default=0)

class Duels(BaseModel):
    total: Optional[int | None] = Field(default=0)
    won: Optional[int | None] = Field(default=0)

class Dribbles(BaseModel):
    attempts: Optional[int | None] = Field(default=0)
    success: Optional[int | None] = Field(default=0)
    past: Optional[int | None] = Field(default=0)

class Fouls(BaseModel):
    drawn: Optional[int | None] = Field(default=0)
    committed: Optional[int | None] = Field(default=0)

class Cards(BaseModel):
    yellow: Optional[int | None] = Field(default=0)
    yellowred: Optional[int | None] = Field(default=0)
    red: Optional[int | None] = Field(default=0)

class Penalty(BaseModel):
    won: Optional[int | None] = Field(default=0)
    committed: Optional[int | None] = Field(default=0)
    scored: Optional[int | None] = Field(default=0)
    missed: Optional[int | None] = Field(default=0)
    saved: Optional[int | None] = Field(default=0)

class Statistics(BaseModel):
    team: Team
    league: League
    games: Games
    substitutes: Optional[Substitutes] = Field(default=None)
    shots: Optional[Shots] = Field(default=None)
    goals: Optional[Goals] = Field(default=None)
    passes: Optional[Passes] = Field(default=None)
    tackles: Optional[Tackles] = Field(default=None)
    duels: Optional[Duels] = Field(default=None)
    dribbles: Optional[Dribbles] = Field(default=None)
    fouls: Optional[Fouls] = Field(default=None)
    cards: Optional[Cards] = Field(default=None)
    penalty: Optional[Penalty] = Field(default=None)
    
class ResponseData(BaseModel):
    player: Player
    statistics: list[Statistics]

class Parameters(BaseModel):
    season: int
    league: int

class TopStatisticsResponse(RapidApiResponse):
    parameters: Parameters
    response: list[ResponseData]
