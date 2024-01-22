from loguru import logger

from app.models.domain.fixture_player_stat import FixturePlayerStat
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository


class FixturePlayerStatRepository(BaseRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("fixture_player_stats")
    
    async def findOne(self, filter: dict) -> FixturePlayerStat:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            FixturePlayerStat: FixturePlayerStat Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        fixture_doc = await self.collection.find_one(filter=filter, projection=projection)
        return FixturePlayerStat.model_validate(fixture_doc)
        
    async def update(self, lineup: FixturePlayerStat) -> None:
        """This method updates fixture lineups documents asynchronously

        Args:
            lineup (FixturePlayerStat): Data to update
        """
        await self.update_bulk([lineup])
        
    async def update_bulk(self, player_stats: list[FixturePlayerStat]):
        """This method updates fixture lineups documents asynchronously

        Args:
            lineups (list[FixturePlayerStat]): Data to update
        """

        logger.debug(f"Updating Fixture Lineup documents")
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league", "fixture_id", "team_id"],
                            datalist=player_stats)