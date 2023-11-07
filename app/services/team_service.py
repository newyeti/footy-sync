from typing import Any
from loguru import logger
from automapper import mapper

from app.api.dependencies.cache import CacheService
from app.services.base_service import BaseService
from app.api.dependencies.rapid_api import RapidApiService
from app.models.schema.team import TeamInRapidApiResponse
from app.models.domain.team import Team
from app.db.repositories.team_repository import TeamRepository

class TeamService(BaseService):

    def __init__(self, 
                 rapid_api_service: RapidApiService,
                 cache_service: CacheService,
                 team_repository: TeamRepository) -> None:
        self.rapid_api_service = rapid_api_service
        self.cache_service = cache_service
        self.team_repository = team_repository


    async def call_api(self, season: int, league_id: int) -> Any:
        logger.info(f"TeamService:fetch_from_api - season={season}, league_id={league_id}")
        api_endpoint = self.rapid_api_service.settings.teams_endpoint
        api_response = await self.rapid_api_service.fetch_from_api(endpoint=api_endpoint, 
                                              season=season, 
                                              league_id=league_id)
        
        logger.debug(api_response.response_data)
        
        teams_obj = TeamInRapidApiResponse.model_validate(api_response.response_data)
        
        logger.debug(f"Parameter: {teams_obj.parameters.league}")
        
        return teams_obj


    def convert_to_domain(self, schema: TeamInRapidApiResponse) -> list[Team]:
        logger.debug("Converting schema to domain model")
        
        teams : list[Team] = []
        
        for i in range(len(schema.response)):
            team = schema.response[i].team
            venue = schema.response[i].venue
            
            team = mapper.to(Team).map(schema, fields_mapping={
                "league_id": schema.parameters.league,
                "season": schema.parameters.season,
                "team_id": team.id,
                "name": team.name,
                "code": team.code,
                "founded": team.founded,
                "country": team.country,
                "logo": team.logo,
                "is_national": team.national,
                "stadium_name": venue.name,
                "stadium_capacity": venue.capacity,
                "stadium_surface": venue.surface,
                "street": venue.address,
                "city": venue.city,
            })
            teams.append(team)
            
        logger.debug(teams)
        return teams


    async def save_in_db(self, teams: list[Team]) -> None:
        logger.debug("Saving team domain models to database")
        await self.team_repository.update_bulk(teams)
        logger.debug("Team domain models saved to database")
    