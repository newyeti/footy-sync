from pydantic import BaseModel, Field
from typing import Optional
from app.models.common import current_date_str

class Goals(BaseModel):
    goals_for: int
    goals_against: int

class Stat(BaseModel):
    played: int
    win: int
    draw: int
    lose: int
    goals: Goals
    
class Team(BaseModel):
    team_id: int = Field(..., title="TeamId", description="Team ID")
    team_name: str = Field(..., title="TeamName", description="Team Name")
    team_logo: Optional[str] = Field(..., title="TeamLogo", description="Team Logo")

class TeamStanding(BaseModel):
    rank: int
    team: Team
    points: Optional[int] = Field(default=0)
    goals_diff: Optional[int] = Field(default=0)
    group: str
    form: Optional[str | None] = Field(default=None)
    status: Optional[str | None] = Field(default=None)
    description: Optional[str | None] = Field(default=None)
    all: Optional[Stat | None ] = Field(default=None)
    home: Optional[Stat | None ] = Field(default=None)
    away: Optional[Stat | None ] = Field(default=None)
    last_updated: Optional[str | None] = Field(default=current_date_str())

class Standings(BaseModel):
    season: int
    league_id: int
    name: str
    country: str
    logo: str
    flag: str
    standings: list[TeamStanding]
    