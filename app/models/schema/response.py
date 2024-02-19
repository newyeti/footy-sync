from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from multidict import CIMultiDictProxy


class ApiResponseStatus(Enum):
    success = "success"
    failed = "failed"


class HttpResponse:
    def __init__(self, headers: CIMultiDictProxy[str], status_code: int, response_data: Any) -> None:
        self.headers = headers
        self.status_code = status_code
        self.response_data = response_data


class ApiResponse(BaseModel):
    season: int
    league_id: int
    fixture_id: Optional[int | None] = None
    service: str
    status: ApiResponseStatus
    message: Optional[str | None] = None
    date: Optional[str|None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "season": 2023,
                    "league_id": 39,
                    "service": "service_name",
                    "status": "success",
                    "message": "Data sychnorized successfully.",
                    "date": "2024-01-01T14:10:26.113Z"
                }
            ]
        }
    }

