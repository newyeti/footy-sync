from pydantic import BaseModel, Field
from typing import Optional

class Team(BaseModel):
    id : int
    name: str
    logo: Optional[str] = Field(default=None)