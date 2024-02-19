from typing import Optional
from pydantic import BaseModel, Field

class Team(BaseModel):
    team_id: int = Field(..., title="TeamId", description="Team ID")
    team_name: str = Field(..., title="TeamName", description="Team Name")
    team_logo: Optional[str] = Field(default=None, title="TeamLogo", description="Team Logo")

class Goal(BaseModel):
    home_team: Optional[int] = Field(default=None, title="HomeTeamGoals", description="Goals scored by home team")
    away_team: Optional[int] = Field(default=None, title="AwayTeamGoals", description="Goals scored by away team")

class Score(BaseModel):
    half_time: Optional[str] = Field(default=None, title="HalfTimeScore", description="Half time score")
    full_time: Optional[str] = Field(default=None, title="FullTimeScore", description="Full time score")
    extra_time: Optional[str] = Field(default=None, title="ExtraTimeScore", description="Scores after extra time")
    penalty: Optional[str] = Field(default=None, title="PenaltyScore", description="Penalty score")
    
class Fixture(BaseModel):
    season: int = Field(default=0,title= "Season")
    league_id: int = Field(..., title="LeagueID")
    fixture_id: int = Field(..., title="FixtureID")
    league_name: str = Field(..., title="LeagueName")
    event_date: str = Field(..., title="EventDate")
    first_half_start: Optional[int] = Field(default=None, title="FirstHalfStartTime")
    second_half_start: Optional[int] = Field(default=None, title="SecondHalfStartTime")
    round: str = Field(..., title="Round")
    status: str = Field(..., title="Status")
    elapsed: Optional[int] = Field(..., title="Elapsed")
    stadium: str = Field(..., title="Stadium")
    city: str = Field(..., title="City")
    referee: Optional[str] = Field(default=None, title="Referee")
    home_team: Team = Field(..., title="HomeTeam")
    away_team: Team = Field(..., title="AwayTeam")
    goals: Goal = Field(..., title="Goals")
    score: Score = Field(..., title="Score")