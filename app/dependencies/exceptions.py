from typing import Any
class ConnectionError(Exception):
    ...

class ServiceException(Exception):
    def __init__(self, name: str, api_url: str, message: Any):
        self.name = name
        self.api_url = api_url
        self.message = message