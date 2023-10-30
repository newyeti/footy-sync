from pydantic import BaseModel
from typing import Optional, Any

class Parameters(BaseModel):
    league: int
    season: int
    
class Paging(BaseModel):
    current: int
    total: int
    
class RapidApiResponse(BaseModel):
    get: str
    parameters: Parameters
    errors: Optional[Any]
    results: int
    paging: Paging
