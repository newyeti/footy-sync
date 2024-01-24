from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import current_date_str

class ShotStat(BaseModel):
    total: Optional[int] = Field(default=0)
    on: Optional[int] = Field(default=0)

class GoalStat(BaseModel):
    total: Optional[int] = Field(default=0)
    conceded: Optional[int] = Field(default=0)
    assists: Optional[int] = Field(default=0)
    saves: Optional[int] = Field(default=0)

class PassStat(BaseModel):
    total: Optional[int] = Field(default=0)
    key: Optional[int] = Field(default=0)
    accuracy: Optional[int] = Field(default=0)

class TackleStat(BaseModel):
    total: Optional[int] = Field(default=0)
    blocks: Optional[int] = Field(default=0)
    interceptions: Optional[int] = Field(default=0)

class DuelStat(BaseModel):
    total: Optional[int] = Field(default=0)
    won: Optional[int] = Field(default=0)

class DribbleStat(BaseModel):
    attempts: Optional[int] = Field(default=0)
    success: Optional[int] = Field(default=0)
    past: Optional[int] = Field(default=0)

class FoulStat(BaseModel):
    drawn: Optional[int] = Field(default=0)
    committed: Optional[int] = Field(default=0)

class CardStat(BaseModel):
    yellow: Optional[int] = Field(default=0)
    red: Optional[int] = Field(default=0)

class PenaltyStat(BaseModel):
    won: Optional[int] = Field(default=0)
    committed: Optional[int] = Field(default=0)
    success: Optional[int] = Field(default=0)
    saved: Optional[int] = Field(default=0)

class FixturePlayerStatistics(BaseModel):
    season: int = Field(default=0, title="Season")
    league_id: int
    fixture_id: int
    event_date: str = Field(default=current_date_str())
    player_id: int
    player_name: str
    team_id: int
    team_name: str
    number: Optional[int]
    position: str
    rating: Optional[float]
    minutes_played: Optional[int]
    captain: Optional[bool]
    substitute: Optional[bool]
    offsides: Optional[int]
    shots: Optional[ShotStat]
    goals: Optional[GoalStat]
    passes: Optional[PassStat]
    tackles: Optional[TackleStat]
    duels: Optional[DuelStat]
    dribbles: Optional[DribbleStat]
    fouls: Optional[FoulStat]
    cards: Optional[CardStat]
    penalty: Optional[PenaltyStat]
