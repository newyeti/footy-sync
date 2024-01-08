from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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
    points: int
    goals_diff: int
    group: str
    form: str
    status: str
    description: str
    all: Stat
    home: Stat
    away: Stat

class Standings(BaseModel):
    season: int
    league_id: int
    name: str
    country: str
    logo: str
    flag: str
    standings: list[TeamStanding]
    update: datetime
    