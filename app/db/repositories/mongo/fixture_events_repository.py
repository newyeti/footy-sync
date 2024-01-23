from loguru import logger

from app.models.domain.fixture_event import FixtureEvent
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository


class FixtureEventRepository(BaseRepository):
    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("fixture_events")
    
    async def findOne(self, filter: dict) -> FixtureEvent:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            FixtureEvent: FixtureEvent Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        fixture_doc = await self.collection.find_one(filter=filter, projection=projection)
        return FixtureEvent.model_validate(fixture_doc)
        
    async def update(self, event: FixtureEvent) -> None:
        """This method updates fixture lineups documents asynchronously

        Args:
            lineup (FixtureEvent): Data to update
        """
        await self.update_bulk([event])
        
    async def update_bulk(self, events: list[FixtureEvent]):
        """This method updates fixture lineups documents asynchronously

        Args:
            lineups (list[FixtureEvent]): Data to update
        """

        logger.debug(f"Updating Fixture Lineup documents")
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league", "fixture_id", "team_id", "player_id", "type", "elapsed", "elapsed_plus"],
                            datalist=events)