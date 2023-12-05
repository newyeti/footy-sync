from google.cloud import bigquery
from app.core.settings.infra import BigQuerySettings
import base64
import os
from loguru import logger


class BigQueryClient:

  def __init__(self, settings: BigQuerySettings) -> None:
    credential_json = ""
    try:

      credential_json = self._create_credential_file(settings.credential)
      os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_json

      self.client = bigquery.Client(
          project=settings.project).from_service_account_json(credential_json)
      self.project_id = settings.project
      self.dataset_ref = bigquery.DatasetReference(
          project=settings.project, dataset_id=settings.dataset)
      self.job_config = bigquery.QueryJobConfig()
      self.job_config.use_query_cache = False

    finally:
      self._remove_credential_file(credential_json)


  def isconnected(self) -> bool:
    api_version = self.client._connection.API_VERSION

    if api_version:
      logger.debug(f"BigQuery API Version: {api_version}")
      return True
    return False

  def _create_credential_file(self, credential_str: str) -> str:
    filename = "credentials.json"
    credentials = base64.b64decode(credential_str).decode("utf-8")

    with open(filename, "w") as file:
      file.write(credentials)

    return filename

  def _remove_credential_file(self, filename: str):
    if os.path.exists(filename):
      os.remove(filename)
