from app.db.repositories.base_repository import BaseRepository
from google.cloud import bigquery
from app.db.clients.bigquery import BigQueryClient

from typing import Any
from loguru import logger
import json


class TeamRepository(BaseRepository):

    def __init__(self, client: BigQueryClient) -> None:
        self.client = client
        self.table_id = "teams"
        self.table_ref = bigquery.TableReference(
            dataset_ref=self.client.dataset_ref, table_id=self.table_id)
        self.query_table = f"""{self.client.project_id}.{self.client.dataset_ref.dataset_id}.{self.table_ref.table_id}"""

    async def findOne(self, filter: dict) -> int:
        team_count_query = f"""SELECT count(*) as count FROM `{self.query_table}` 
                                WHERE season = {filter["season"]} AND 
                                    league_id = {filter["league_id"]} AND
                                    team_id = {filter["team_id"]}                                    
                            """

        query_job = self.client.client.query(
            query=team_count_query, project=self.client.client.project, job_config=self.client.job_config
        )
        results = query_job.result().to_dataframe()
        return results['count'][0]

    async def update(self, data: dict) -> None:
        rows_to_insert = [data]

        # Make an API request.
        errors = self.client.client.insert_rows_json(
            self.query_table, json_rows=rows_to_insert)

        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))


    async def update_bulk(self, data: list[Any]) -> None:

        # Make an API request.
        errors = self.client.client.insert_rows_json(
            self.query_table, json_rows=data)

        if errors == []:
            logger.info(f"New rows have been added to {self.query_table}.")
        else:
            logger.error(
                "Encountered errors while inserting rows: {}".format(errors))
