from pydantic import BaseModel, Field
from typing import Optional

from app.models.common import current_date_str

class Player(BaseModel):
    player_id : int
    player_name : str
    number: int
    pos: str
    grid: Optional[str | None] = None

class FixtureLineup(BaseModel):
    season: int = Field(default=0, title="Season")
    league_id : int
    fixture_id: int
    coach_id: int
    coach_name: str
    formation: str
    team_id: int
    team_name: str
    team_player_color: str
    team_goalkeeper_color: str
    startingXI: list[Player]
    substitutes: list[Player]
    
