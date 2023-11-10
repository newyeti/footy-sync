from datetime import datetime
from loguru import logger
from pymongo import UpdateOne

from app.models.domain.team import Team
from app.db.clients.mongo import MongoClient
from app.db.repositories.base_repository import BaseRepository


class TeamRepository(BaseRepository):

    def __init__(self, client: MongoClient) -> None:
        self.client = client
        self.collection = self.client.db.get_collection("teams")

    async def findOne(self, filter: dict) -> Team:
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

    async def update(self, t: Team) -> None:
        """This method updates teams data asynchronously

        Args:
            filter (dict): Filter
            data (dict): Data to update
        """
        filter_ = {
            "season": t.season,
            "league_id": t.league_id,
            "team_id": t.team_id
        }

        update_ = {
            "$set": t.model_dump(),
            "$currentDate": {
                "updatedAt": True
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
            }
        }

        await self.collection.update_one(filter_, update_, upsert=True)

    async def update_bulk(self, teams: list[Team]):
        """This method updates teams data asynchronously

        Args:
            filter (dict): Filter
            teams (list[Team]): Data to update
        """

        logger.debug(f"Updating document for {filter}")

        BATCH_SIZE = len(teams)
        updates = list()

        for t in teams:
            filter_ = {
                "season": t.season,
                "league_id": t.league_id,
                "team_id": t.team_id
            }

            update_ = {
                "$set": t.model_dump(),
                "$currentDate": {
                    "updatedAt": True
                },
                "$setOnInsert": {
                    "createdAt": datetime.utcnow()
                }
            }

            u = UpdateOne(filter_, update_, upsert=True)
            updates.append(u)

            if len(updates) > BATCH_SIZE:
                await self.collection.bulk_write(updates, ordered=False)
                updates = list()

        if len(updates) > 0:
            await self.collection.bulk_write(updates, ordered=False)
