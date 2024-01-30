from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class PlayerStatCategory(str, Enum):
    SCORER = "top_scorers"
    ASSIST = "assists"
    YELLOW_CARD = "yellow_cards"
    RED_CARD = "red_cards"

class Brith(BaseModel):
    date: Optional[str | None] = Field(default=None)
    place: Optional[str | None] = Field(default=None)
    country: Optional[str | None] = Field(default=None)

class PlayerDetail(BaseModel):
    firstname: str
    lastname: str
    birth: Optional[Brith]
    nationality: Optional[str | None] = Field(default=None)
    height: Optional[str | None] = Field(default=None)
    weight: Optional[str | None] = Field(default=None)
    injured: Optional[bool | None] = Field(default=False)
    photo: Optional[str | None] = Field(default=None)

class Games(BaseModel):
    appearences: Optional[int | None]
    lineups: Optional[int | None]
    minutes: Optional[int | None]
    number: Optional[int]
    position: Optional[str | None]
    rating: Optional[str | None]
    captain: Optional[bool | None] = Field(default=False)

class Substitutes(BaseModel):
    in_: Optional[int | None] = Field(default=0, serialization_alias="in")
    out: Optional[int | None] = Field(default=0)
    bench: Optional[int | None] = Field(default=0)        

class Shots(BaseModel):
    total: Optional[int | None] = Field(default=0)
    on: Optional[int | None] = Field(default=0)
    
class Goals(BaseModel):
    total: Optional[int | None] = Field(default=0)
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

class Player(BaseModel):
    season: int = Field(default=0, title="Season")
    league_id: int 
    category: str
    player_id: int
    player_name: str
    detail: PlayerDetail
    team_id: int
    team_name: str
    games: Games
    substitutes: Optional[Substitutes|None] = None
    shots: Optional[Shots|None] = None
    goals: Optional[Goals|None] = None
    passes: Optional[Passes|None] = None
    tackles: Optional[Tackles|None] = None
    duels: Optional[Duels|None] = None
    dribbles: Optional[Dribbles|None] = None
    fouls: Optional[Fouls|None] = None
    cards: Optional[Cards|None] = None
    penalty: Optional[Penalty|None] = None

