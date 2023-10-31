from abc import abstractmethod, ABC
from typing import Any


class BaseRepository(ABC):
    
    @abstractmethod
    async def findOne(self, filter: dict) -> Any:
        ...
        
    @abstractmethod
    async def update(self, data: Any) -> None:
        ...
        
    @abstractmethod
    async def update_bulk(self, data: list[Any]) -> None:
        ...