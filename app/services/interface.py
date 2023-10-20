from abc import ABC, abstractmethod
from typing import Any



class IService(ABC):

    @abstractmethod
    async def sync(self, season: int, league_id: int) -> Any:
        ...

    @abstractmethod
    def convert_to_domain(self, schema: Any) -> Any:
        ...

    @abstractmethod
    async def save_in_db(self, domain: Any) -> None:
        ...
    

class ApiService(ABC):
    @abstractmethod
    async def fetch_from_api(self,
                             endpoint: str,
                             season: int, 
                             league_id: int) -> Any:
        ...