from loguru import logger

from app.models.domain.fixture_lineup import FixtureLineup
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository


class FixtureLineupRepository(BaseRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("fixture_lineups")
    
    async def findOne(self, filter: dict) -> FixtureLineup:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            FixtureLineup: FixtureLineup Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        fixture_doc = await self.collection.find_one(filter=filter, projection=projection)
        return FixtureLineup.model_validate(fixture_doc)
        
    async def update(self, lineup: FixtureLineup) -> None:
        """This method updates fixture lineups documents asynchronously

        Args:
            lineup (FixtureLineup): Data to update
        """
        await self.update_bulk([lineup])
        
    async def update_bulk(self, lineups: list[FixtureLineup]):
        """This method updates fixture lineups documents asynchronously

        Args:
            lineups (list[FixtureLineup]): Data to update
        """

        logger.debug(f"Updating Fixture Lineup documents")
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league_id", "fixture_id", "team_id"],
                            datalist=lineups)