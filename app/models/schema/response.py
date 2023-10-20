from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ApiResponseStatus(Enum):
    success = "success"
    failed = "failed"


class ApiResponse(BaseModel):
    season: int
    league_id: int
    service: str
    status: ApiResponseStatus
    message: Optional[str | None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "season": 2023,
                    "league_id": 39,
                    "service": "teams",
                    "status": "success",
                    "message": "Data sychnorized successfully."
                }
            ]
        }
    }

