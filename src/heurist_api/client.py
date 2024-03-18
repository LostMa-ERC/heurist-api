import requests
from typing import ByteString

from heurist_api.url_builder import URLBuilder


class HeuristAPIClient:
    """Client for Heurist API."""

    def __init__(self, database_name: str, session_id: str) -> None:
        self.database_name = database_name
        self.session_id = session_id
        self.cookie = {"heurist-sessionid": session_id}
        self.url_builder = URLBuilder(database_name=database_name)

    def get_records(
        self, record_type_id: str | int, format: str = "xml"
    ) -> bytes | None:
        url = self.url_builder.record(record_type_id=record_type_id, format=format)
        return self.request_bytes(url)

    def get_structure(self) -> bytes | None:
        url = self.url_builder.structure
        return self.request_bytes(url)

    def request_bytes(self, url: str) -> ByteString | None:
        response = requests.get(url, cookies=self.cookie)
        if response.status_code == 200:
            return self.validator(response.content)

    def validator(self, byte_string: ByteString) -> ByteString | None:
        if "Cannot connect to database" != byte_string.decode("utf-8"):
            return byte_string
