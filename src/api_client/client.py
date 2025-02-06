"""Heurist API client"""

import json
from typing import ByteString, Literal

from src.api_client.exceptions import APIException
from src.api_client.session import HeuristRequestSession
from src.api_client.url_builder import URLBuilder


class HeuristAPIClient:
    """Client for Heurist API."""

    def __init__(self, database_name: str, login: str, password: str) -> None:
        self.database_name = database_name
        self.url_builder = URLBuilder(database_name=database_name)
        self.__login = login  # Private variable
        self.__password = password  # Private variable

    def get_response_content(self, url: str) -> ByteString | None:
        """Request resources from the Heurist server.

        Args:
            url (str): Heurist API entry point.

        Returns:
            ByteString | None: Binary response returned from Heurist server.
        """

        kwargs = {
            "db": self.database_name,
            "login": self.__login,
            "password": self.__password,
        }
        with HeuristRequestSession(**kwargs) as session:
            response = session.get(url, timeout=10)
            if not response:
                raise APIException("No response")
            elif not response.status_code == 200:
                raise APIException(f"Status {response.status_code}")
            elif "Cannot connect to database" == response.content.decode("utf-8"):
                raise APIException("Could not connect to database.")
            else:
                return response.content

    def get_records(
        self,
        record_type_id: int,
        form: Literal["xml", "json"] = "json",
        users: tuple[int] = (),
    ) -> bytes | list | None:
        """Request all records of a certain type and in a certain data format.

        Examples:
            >>> import json
            >>> from src.api_client import HeuristClient
            >>>
            >>>
            >>> client = HeuristClient()
            >>> res = client.get_records(101)
            >>> len(res) > 0
            True

        Args:
            record_type_id (int): Heurist ID of targeted record type.
            form (Literal["xml", "json"], optional): Data format for requested
                records. Defaults to "json".
            users (tuple): Array of IDs of users who added the target records.

        Returns:
            bytes | list | None: If XML, binary response returned from Heurist
                server, else JSON array.
        """

        url = self.url_builder.get_records(
            record_type_id=record_type_id, form=form, users=users
        )
        if form == "json":
            content = self.get_response_content(url)
            json_string = content.decode("utf-8")
            all_records = json.loads(json_string)["heurist"]["records"]
            # Filter out linked records of a not the target type
            correct_ids = [
                r for r in all_records if r["rec_RecTypeID"] == str(record_type_id)
            ]
            # Filter out records by non-targeted users
            if users and len(users) > 0:
                return [r for r in correct_ids if int(r["rec_AddedByUGrpID"]) in users]
            else:
                return correct_ids
        else:
            return self.get_response_content(url)

    def get_relationship_markers(
        self, form: Literal["xml", "json"] = "xml"
    ) -> bytes | list | None:
        return self.get_records(record_type_id=1, form=form)

    def get_structure(self) -> bytes | None:
        """Request the Heurist database's overall structure in XML format.

        Examples:
            >>> from src.api_client import HeuristClient
            >>>
            >>>
            >>> client = HeuristClient()
            >>> res = client.get_structure()
            >>> type(res)
            <class 'bytes'>

        Returns:
            bytes | list | None: If XML, binary response returned from Heurist server,
            else JSON array.
        """
        url = self.url_builder.get_db_structure()
        return self.get_response_content(url)
