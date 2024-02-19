from loguru import logger
from opentelemetry import trace
from  motor.motor_asyncio import AsyncIOMotorCursor

from app.services.fixtures_service import FixtureService
from app.services.fixture_lineup_service import FixtureLineupService
from app.services.fixture_player_stats_service import FixturePlayerStatsService
from app.services.fixture_events_service import FixtureEventsService
from app.db.repositories.mongo.fixture_repository import FixtureRepository

from app.models.domain.fixture import Fixture


class FixtureTemplateService:
    def __init__(self,
                 fixture_service: FixtureService,
                 fixture_lineup_service: FixtureLineupService,
                 fixture_events_service: FixtureEventsService,
                 fixture_player_stats_service: FixturePlayerStatsService,
                 fixture_repository: FixtureRepository
                 ) -> None:
        self.fs = fixture_service
        self.fls = fixture_lineup_service
        self.fes = fixture_events_service
        self.fpss = fixture_player_stats_service
        self.fr = fixture_repository
        self.tracer = trace.get_tracer(__name__)
    
    async def update_by_date(self, 
                             season: int, 
                             league_id: int,
                             fromDate: str,
                             toDate: str):
        """Update the fixture, lineups , events and statistics
        """
        
        logger.debug(f"finding fixtures between {fromDate} and {toDate}")
        
        with self.tracer.start_as_current_span(f"update.fixture.by.date"):
            cursor: AsyncIOMotorCursor = self.fr.find({ # type: ignore
                "season": season,
                "league_id": league_id,
                "event_date": {
                    "$gte": fromDate,
                    "$lt": toDate 
                },
            })
            fixtures = await cursor.to_list(None) 
        
        for f in fixtures:
            fixture = Fixture.model_validate(f)
            logger.info(fixture)
            await self.fs.execute(season=season,
                            league_id=league_id,
                            fixture_id=fixture.fixture_id)
            await self.fls.execute(season=season,
                            league_id=league_id,
                            fixture_id=fixture.fixture_id)   
            await self.fes.execute(season=season,
                            league_id=league_id,
                            fixture_id=fixture.fixture_id)
            await self.fpss.execute(season=season,
                            league_id=league_id,
                            fixture_id=fixture.fixture_id)
        
        
    def update_by_status(self):
        pass
    
    