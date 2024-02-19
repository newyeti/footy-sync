from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class PlayerStatCategory(str, Enum):
    SCORER = "top_scorers"
    ASSIST = "top_assists"
    YELLOW_CARD = "yellow_cards"
    RED_CARD = "red_cards"

class Brith(BaseModel):
    date: Optional[str | None] = Field(default=None)
    place: Optional[str | None] = Field(default=None)
    country: Optional[str | None] = Field(default=None)

class PlayerDetail(BaseModel):
    firstname: str
    lastname: str
    birth: Optional[Brith|None] = Field(default=None)
    nationality: Optional[str | None] = Field(default=None)
    height: Optional[str | None] = Field(default=None)
    weight: Optional[str | None] = Field(default=None)
    injured: Optional[bool | None] = Field(default=False)
    photo: Optional[str | None] = Field(default=None)

class Games(BaseModel):
    appearences: Optional[int | None]
    lineups: Optional[int | None]
    minutes: Optional[int | None]
    number: Optional[int | None]
    position: Optional[str | None]
    rating: Optional[str | None]
    captain: Optional[bool | None] = Field(default=False)

class Substitutes(BaseModel):
    in_: Optional[int | None] = Field(default=None, serialization_alias="in")
    out: Optional[int | None] = Field(default=None)
    bench: Optional[int | None] = Field(default=None)        

class Shots(BaseModel):
    total: Optional[int | None] = Field(default=None)
    on: Optional[int | None] = Field(default=None)
    
class Goals(BaseModel):
    total: Optional[int | None] = Field(default=None)
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

class Player(BaseModel):
    season: int = Field(default=None, title="Season")
    league_id: int 
    category: str
    player_id: int
    player_name: str
    detail: Optional[PlayerDetail|None]
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

