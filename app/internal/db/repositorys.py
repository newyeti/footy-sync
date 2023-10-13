from app.internal.db.mongo_client import MongoClient

class TeamRepository:
    
    def __init__(self, db: MongoClient) -> None:
        self.db = db
    
    