"""
Heurist API client wrapper
"""

import json
import os
from pathlib import Path
from typing import ByteString, Literal

from dotenv import find_dotenv, load_dotenv

from heurist.client.session import HeuristRequestSession
from heurist.client.url_builder import URLBuilder


class APIException(Exception):
    """Problem calling Heurist API."""


class HeuristAPIClient:
    """Client for Heurist API."""

    def __init__(self, database_name: str, login: str, password: str) -> None:
        self.database_name = database_name
        self.url_builder = URLBuilder(database_name=database_name)
        self.__login = login  # Private variable
        self.__password = password  # Private variable

    def get_response_content(self, url: str) -> ByteString | None:
        """Request resources from the Heurist server.

        Examples:
            >>> from heurist.client import HeuristClient
            >>>
            >>>
            >>> url = "https://heurist.huma-num.fr/heurist/export/xml/flathml.php?q=sortby%3A-m&a=1&db={}&depth=0"
            >>> client = HeuristClient()
            >>>
            >>> # Test valid URL
            >>> res = client.get_response_content(url=url.format(client.database_name))
            >>> type(res)
            <class 'bytes'>
            >>>
            >>> # Test invalid URL
            >>> client.get_response_content(url=url.format("missing_database"))
            Traceback (most recent call last):
                ...
            heurist.client.client.APIException: Could not connect to database.

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
        self, record_type_id: int, form: Literal["xml", "json"] = "json"
    ) -> bytes | list | None:
        """Request all records of a certain type and in a certain data format.

        Examples:
            >>> import json
            >>> from heurist.client import HeuristClient
            >>>
            >>>
            >>> client = HeuristClient()
            >>> res = client.get_records(101)
            >>> len(res) > 0
            True

        Args:
            record_type_id (int): Heurist ID of targeted record type.
            form (Literal["xml", "json"], optional): Data format for requested records. Defaults to "json".

        Returns:
            bytes | list | None: If XML, binary response returned from Heurist server, else JSON array.
        """

        url = self.url_builder.get_records(record_type_id=record_type_id, form=form)
        if form == "json":
            content = self.get_response_content(url)
            json_string = content.decode("utf-8")
            records = json.loads(json_string)["heurist"]["records"]
            return [r for r in records if r["rec_RecTypeID"] == str(record_type_id)]
        else:
            return self.get_response_content(url)

    def get_relationship_markers(
        self, form: Literal["xml", "json"] = "xml"
    ) -> bytes | list | None:
        return self.get_records(record_type_id=1, form=form)

    def get_structure(self) -> bytes | None:
        """Request the Heurist database's overall structure in XML format.

        Examples:
            >>> from heurist.client import HeuristClient
            >>>
            >>>
            >>> client = HeuristClient()
            >>> res = client.get_structure()
            >>> type(res)
            <class 'bytes'>

        Returns:
            bytes | list | None: If XML, binary response returned from Heurist server, else JSON array.
        """
        url = self.url_builder.get_db_structure()
        return self.get_response_content(url)


class HeuristAPIClientWrapper(HeuristAPIClient):
    def __init__(
        self,
        database_name: str | None = None,
        login: str | None = None,
        password: str | None = None,
        testing: bool = False,
    ) -> None:
        """Build the HeuristAPIClient from declared or environment variables.

        Args:
            database_name (str | None): Name of the Heurist database.
            login (str | None): Heurist user's account name.
            password (str | None): Heurist user's password.
        """

        if not testing:
            loaded_env_vars = load_dotenv(find_dotenv())
            if not loaded_env_vars:
                load_dotenv(find_dotenv(Path.cwd().joinpath(".env")))
            if not database_name:
                database_name = os.environ["DB_NAME"]
            if not login:
                login = os.environ["DB_LOGIN"]
            if not password:
                password = os.environ["DB_PASSWORD"]
        else:
            database_name = "test_db"
            login = "test_user"
            password = "test_password"
        super().__init__(database_name, login, password)
