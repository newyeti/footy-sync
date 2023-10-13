from app.internal.db.mongo import MongoClient

class TeamRepository:
    
    def __init__(self, db: MongoClient) -> None:
        self.db = db
    
    