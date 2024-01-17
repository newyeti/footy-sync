import datetime
import time
from typing import Optional, Any

from pydantic import BaseModel, Field, validator

def current_date_str():
    datetime_obj = datetime.datetime.fromtimestamp(time.time())
    formatted_date = datetime_obj.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    return formatted_date

class DateTimeModelMixin(BaseModel):
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None

    # @validator
    # def default_datetime(
    #         cls,
    #         value: datetime.datetime
    #         ) -> datetime.datetime:
    #     return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id_: int = Field(0, alias="id")

    
class Paging(BaseModel):
    current: int
    total: int

class RapidApiResponse(BaseModel):
    get: str
    errors: Optional[Any]
    results: int
    paging: Paging
