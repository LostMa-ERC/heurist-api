"""Heurist API client"""

import json
from typing import ByteString, Literal

import requests
from heurist.api.constants import MAX_RETRY, READTIMEOUT
from heurist.api.exceptions import APIException, ReadTimeout
from heurist.api.url_builder import URLBuilder
from heurist.api.utils import log_attempt_number
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
)


class HeuristAPIClient:
    """
    Client for Heurist API.
    """

    def __init__(
        self,
        database_name: str,
        session: requests.Session,
        timeout_seconds: int | None = READTIMEOUT,
    ) -> None:
        self.database_name = database_name
        self.url_builder = URLBuilder(database_name=database_name)
        self.session = session
        self.timeout = timeout_seconds

    @retry(
        retry=retry_if_exception_type(requests.exceptions.ReadTimeout),
        stop=stop_after_attempt(MAX_RETRY),
        after=log_attempt_number,
    )
    def call_heurist_api(self, url: str) -> ByteString | None:
        response = self.session.get(url, timeout=(self.timeout))
        return response

    def get_response_content(self, url: str) -> ByteString | None:
        """Request resources from the Heurist server.

        Args:
            url (str): Heurist API entry point.

        Returns:
            ByteString | None: Binary response returned from Heurist server.
        """

        try:
            response = self.call_heurist_api(url=url)
        except RetryError:
            e = ReadTimeout(url=url, timeout=self.timeout)
            raise SystemExit(e)
        if not response:
            e = APIException("No response.")
            raise SystemExit(e)
        elif response.status_code != 200:
            e = APIException(f"Status {response.status_code}")
            raise SystemExit(e)
        elif "Cannot connect to database" == response.content.decode("utf-8"):
            e = APIException("Could not connect to database.")
            raise SystemExit(e)
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
