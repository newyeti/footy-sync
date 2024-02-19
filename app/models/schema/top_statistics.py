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
    age: Optional[int | None] = Field(default=None)
    birth: Optional[Brith|None] = Field(default=None)
    nationality: Optional[str | None] = Field(default=None)
    height: Optional[str | None] = Field(default=None)
    weight: Optional[str | None] = Field(default=None)
    injured: Optional[bool] = Field(default=False)
    photo: Optional[str | None] = Field(default=None)

class Games(BaseModel):
    appearences: Optional[int | None] = Field(default=None)
    lineups: Optional[int | None] = Field(default=None)
    minutes: Optional[int | None] = Field(default=None)
    number: Optional[int] = Field(default=None)
    position: Optional[str | None] = Field(default=None)
    rating: Optional[str | None] = Field(default=None)
    captain: Optional[bool] = Field(default=False)

class Substitutes(BaseModel):
    in_: Optional[int | None] = Field(default=None, alias="in")
    out: Optional[int | None] = Field(default=None)
    bench: Optional[int | None] = Field(default=None)

class Shots(BaseModel):
    total: Optional[int|None] = Field(default=None)
    on: Optional[int|None] = Field(default=None)

class Goals(BaseModel):
    total: Optional[int|None] = Field(default=None)
    conceded: Optional[int | None] = Field(default=None)
    assists: Optional[int | None] = Field(default=None)
    saves: Optional[int | None] = Field(default=None) 

class Passes(BaseModel):
    total: Optional[int | None] = Field(default=None)
    key: Optional[int | None] = Field(default=None)
    accuracy: Optional[int | None] = Field(default=None)

class Tackles(BaseModel):
    total: Optional[int | None] = Field(default=None)
    blocks: Optional[int | None] = Field(default=None)
    interceptions: Optional[int | None] = Field(default=None)

class Duels(BaseModel):
    total: Optional[int | None] = Field(default=None)
    won: Optional[int | None] = Field(default=None)

class Dribbles(BaseModel):
    attempts: Optional[int | None] = Field(default=None)
    success: Optional[int | None] = Field(default=None)
    past: Optional[int | None] = Field(default=None)

class Fouls(BaseModel):
    drawn: Optional[int | None] = Field(default=None)
    committed: Optional[int | None] = Field(default=None)

class Cards(BaseModel):
    yellow: Optional[int | None] = Field(default=None)
    yellowred: Optional[int | None] = Field(default=None)
    red: Optional[int | None] = Field(default=None)

class Penalty(BaseModel):
    won: Optional[int | None] = Field(default=None)
    committed: Optional[int | None] = Field(default=None)
    scored: Optional[int | None] = Field(default=None)
    missed: Optional[int | None] = Field(default=None)
    saved: Optional[int | None] = Field(default=None)

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
