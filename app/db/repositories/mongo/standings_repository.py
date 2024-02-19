from loguru import logger

from app.models.domain.standings import Standings
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository

class StandingsRepository(BaseRepository):

    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("standings")

    async def findOne(self, filter: dict) -> Standings:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            Team: Team Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        team_document = await self.collection.find_one(filter=filter, projection=projection)
        return team_document

    async def update(self, standings: Standings) -> None:
        """This method updates teams data asynchronously

        Args:
            data (dict): Data to update
        """
        self.update_bulk(standings==[standings])

    async def update_bulk(self, standings: list[Standings]):
        """This method updates teams data asynchronously

        Args:
            teams (list[Team]): Data to update
        """
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league_id"],
                            datalist=standings)
