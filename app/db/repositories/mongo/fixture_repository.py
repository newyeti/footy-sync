from datetime import datetime
from loguru import logger
from pymongo import UpdateOne

from app.models.domain.fixture import Fixture
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository


class FixtureRepository(BaseRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("fixtures")
    
    async def findOne(self, filter: dict) -> Fixture:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            Team: Fixture Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        fixture_doc = await self.collection.find_one(filter=filter, projection=projection)
        return fixture_doc
        
    async def update(self, f: Fixture) -> None:
        """This method updates teams data asynchronously

        Args:
            filter (dict): Filter
            data (dict): Data to update
        """
        await self.update_bulk([f])
        
    async def update_bulk(self, fixtures: list[Fixture]):
        """This method updates teams data asynchronously

        Args:
            filter (dict): Filter
            teams (list[Team]): Data to update
        """

        logger.debug(f"Updating document for {filter}")
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league", "fixture_id"],
                            datalist=fixtures)