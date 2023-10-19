from abc import ABC, abstractmethod
from typing import Any



class IService(ABC):

    @abstractmethod
    async def sync(self, season: int, league_id: int) -> Any:
        ...

    @abstractmethod
    async def save_in_db(self) -> None:
        ...
    

class ApiService(ABC):
    @abstractmethod
    async def fetch_from_api(self,
                             settings: Any, 
                             uri,
                             season: int, 
                             league_id: int) -> Any:
        ...