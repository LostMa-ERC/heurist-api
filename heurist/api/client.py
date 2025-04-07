"""Heurist API client"""

import json
from typing import Literal, ByteString
import requests
import time

from heurist.api.exceptions import APIException
from heurist.api.url_builder import URLBuilder


class HeuristAPIClient:
    """
    Client for Heurist API.
    """

    def __init__(self, database_name: str, session: requests.Session) -> None:
        self.database_name = database_name
        self.url_builder = URLBuilder(database_name=database_name)
        self.session = session

    def get_response_content(self, url: str) -> ByteString | None:
        """Request resources from the Heurist server.

        Args:
            url (str): Heurist API entry point.

        Returns:
            ByteString | None: Binary response returned from Heurist server.
        """

        try:
            response = self.session.get(url, timeout=(0.2, 15))
        except requests.exceptions.ReadTimeout as e:
            # Retry after waiting a few seconds
            print("Read timeout. Retrying Heurist server.")
            time.sleep(5)
            response = self.session.get(url, timeout=(0.2, 15))
            raise e
        if not response:
            raise APIException("No response.")
        elif response.status_code != 200:
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

    def get_structure(self) -> bytes | None:
        """Request the Heurist database's overall structure in XML format.

        Returns:
            bytes | list | None: If XML, binary response returned from Heurist server,
            else JSON array.
        """
        url = self.url_builder.get_db_structure()
        return self.get_response_content(url)

    def get_relationship_markers(
        self, form: Literal["xml", "json"] = "xml"
    ) -> bytes | list | None:
        return self.get_records(record_type_id=1, form=form)
