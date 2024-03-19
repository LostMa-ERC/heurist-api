# Heurist API client wrapper


from typing import ByteString
import requests

from heurist_api.url_builder import URLBuilder


class HeuristAPIClient:
    """Client for Heurist API."""

    def __init__(self, database_name: str, session_id: str) -> None:
        """_summary_

        Args:
            database_name (str): _description_
            session_id (str): _description_
        """
        self.database_name = database_name
        self.session_id = session_id
        self.cookie = {"heurist-sessionid": session_id}
        self.url_builder = URLBuilder(database_name=database_name)

    def get_records(self, record_type_id: str | int, form: str = "xml") -> bytes | None:
        """_summary_

        Args:
            record_type_id (str | int): _description_
            form (str, optional): _description_. Defaults to "xml".

        Returns:
            bytes | None: _description_
        """
        url = self.url_builder.record(record_type_id=record_type_id, form=form)
        return self.request_bytes(url)

    def get_structure(self) -> bytes | None:
        """_summary_

        Returns:
            bytes | None: _description_
        """
        url = self.url_builder.structure
        return self.request_bytes(url)

    def request_bytes(self, url: str) -> ByteString | None:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            ByteString | None: _description_
        """
        result = None
        response = requests.get(url, cookies=self.cookie, timeout=10)
        if response and response.status_code == 200:
            result = self.validator(response.content)
        return result

    def validator(self, byte_string: ByteString) -> ByteString | None:
        """_summary_

        Args:
            byte_string (ByteString): _description_

        Returns:
            ByteString | None: _description_
        """
        result = byte_string
        if "Cannot connect to database" == byte_string.decode("utf-8"):
            result = None
        return result
