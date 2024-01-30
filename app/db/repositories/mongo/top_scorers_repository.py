from loguru import logger

from app.models.domain.top_statistics import Player
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository
from motor.motor_asyncio import AsyncIOMotorCursor

class TopScorersRepository(BaseRepository):

    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("player_stats")

    async def findOne(self, filter: dict) -> Player:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            Team: Player Document
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        team_document = await self.collection.find_one(filter=filter, projection=projection)
        return team_document
    
    def find(self, filter: dict) -> AsyncIOMotorCursor:
        """This methods find a document asynchronously

        Args:
            filter (dict): Filter

        Returns:
            Team: List of Player Documents
        """
        logger.debug(f"finding document for {filter}")

        projection = {
            "_id": False  # Do not retrun id
        }

        player_documents = self.collection.find(filter=filter, projection=projection)
        return player_documents
    

    async def update(self, player: Player) -> None:
        """This method updates players data asynchronously

        Args:
            data (dict): Data to update
        """
        self.update_bulk(players=[player])

    async def update_bulk(self, players: list[Player]):
        """This method updates players data asynchronously

        Args:
            players (list[Player]): Data to update
        """
        
        await self.updateDocument(collection=self.collection, 
                            filter_strs=["season", "league_id", "category", "player_id"],
                            datalist=players)

    async def delete_bulk(self, players: list[Player]):
        """This method updates players data asynchronously

        Args:
            players (list[Player]): Data to delete
        """
        
        for p in players:
            await self.collection.delete_one({
                "season": p.season,
                "league_id": p.league_id,
                "category": p.category,
                "player_id": p.player_id
            })
        
        