from pydantic import BaseModel
from typing import Optional
from enum import Enum


class CommonPathParams:
    def __init__(self, season: int, league_id: int) -> None:
        self.season = season
        self.league_id = league_id


