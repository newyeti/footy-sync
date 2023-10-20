from multidict import CIMultiDictProxy
from typing import Any


class HttpApiResponse:
    def __init__(self, headers: CIMultiDictProxy[str], status_code: int, response_data: Any) -> None:
        self.headers = headers
        self.status_code = status_code
        self.response_data = response_data
