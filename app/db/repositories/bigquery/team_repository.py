from app.db.repositories.base_repository import BaseRepository
from google.cloud import bigquery
from app.db.clients.bigquery import BigQueryClient

from typing import Any
from loguru import logger


class TeamRepository(BaseRepository):

    def __init__(self, client: BigQueryClient) -> None:
        self.client = client
        self.table_id = "teams"
        self.table_ref = bigquery.TableReference(
            dataset_ref=self.client.dataset_ref, table_id=self.table_id)
        self.query_table = f"{self.client.project_id}.{self.client.dataset_ref.dataset_id}.{self.table_ref.table_id}"

    async def findOne(self, filter: dict) -> Any:
        team_count_query = f"SELECT count(*) as count FROM `{self.query_table}` WHERE season = 2022 AND league_id = 39"

        query_job = self.client.client.query(
            query=team_count_query, project=self.client.client.project, job_config=self.client.job_config
        )
        results = query_job.result().to_dataframe()

        logger.info(results['count'])

    async def update(self, data: Any) -> None:
        ...

    async def update_bulk(self, data: list[Any]) -> None:
        ...
