import datetime

from pydantic import BaseModel, ConfigDict

def convert_datetime(val: datetime.datetime) -> str:
        return val.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    

class RWModel(BaseModel): 
    model_config = ConfigDict(
            json_encoders={datetime.datetime: convert_datetime}
        )
