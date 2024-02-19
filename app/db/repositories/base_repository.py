from abc import abstractmethod, ABC
from typing import Any, Union
from datetime import datetime
from pymongo import UpdateOne
from motor.core import AgnosticCollection


class BaseRepository(ABC):
    
    BATCH_SIZE = 50

    @abstractmethod
    async def findOne(self, filter: dict) -> Any:
        ...
        
    @abstractmethod
    async def update(self, data: Any) -> None:
        ...
        
    @abstractmethod
    async def update_bulk(self, data: list[Any]) -> None:
        ...
    
    
    async def updateDocument(self, 
                            collection: Union[str, AgnosticCollection],
                            filter_strs: list[str], 
                            datalist: list[Any]):
        
        if datalist is None:
            return
        
        updates = list()
        
        for data in datalist:
            filter = {}
            obj_dict = data.__dict__
            
            for str in filter_strs:
                if str in obj_dict:
                    filter[str] = obj_dict[str]
            
            update_ = self.update_conf(data)
            u = UpdateOne(filter, update_, upsert=True)
            updates.append(u)

            if len(updates) > self.BATCH_SIZE:
                await collection.bulk_write(updates, ordered=False)
                updates = list()
                
        if len(updates) > 0:
            await collection.bulk_write(updates, ordered=False)
            
     
    def update_conf(self, obj: Any) -> None:
        return {
            "$set": obj.model_dump(by_alias=True),
            "$currentDate": {
                "updatedAt": True
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
            }
        }