from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import current_date_str

class Player(BaseModel):
    player_id : int
    player_name : str
    number: Optional[int | None] = None
    pos: Optional[str | None] = None
    grid: Optional[str | None] = None

class FixtureLineup(BaseModel):
    season: int = Field(default=0, title="Season")
    league_id : int
    fixture_id: int
    event_date: Optional[str | None] = Field(default=current_date_str())
    coach_id: Optional[int | None] = None
    coach_name: Optional[str | None] = None
    formation: Optional[str | None] = None
    team_id: int
    team_name: str
    team_player_color: Optional[str | None] = None
    team_goalkeeper_color: Optional[str | None] = None
    startingXI: list[Player]
    substitutes: list[Player]
    
