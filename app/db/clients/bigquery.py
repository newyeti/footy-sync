from google.cloud import bigquery
from google.oauth2 import service_account
from app.core.settings.infra import BigQuerySettings
import base64
import os
from loguru import logger


class BigQueryClient:

  def __init__(self, settings: BigQuerySettings) -> None:
    filename = "credentials.json"
    credentials = base64.b64decode(settings.credential).decode("utf-8")
    with open(filename, "w") as file:
      file.write(credentials)

    self.client = bigquery.Client(
        project=settings.project).from_service_account_json(filename)

    if os.path.exists(filename):
      os.remove(filename)

  def isconnected(self) -> bool:
    api_version = self.client._connection.API_VERSION

    if api_version:
      logger.debug(f"BigQuery API Version: {api_version}")
      return True
    return False
