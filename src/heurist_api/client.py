# Heurist API client wrapper
import click
from typing import ByteString
import requests
from requests import Session
from dotenv import load_dotenv, find_dotenv
import os

from heurist_api.url_builder import URLBuilder


class HeuristSession:
    def __init__(self, db: str, login: str, password: str) -> None:
        self.db = db
        self.login = login
        self.password = password

    def __enter__(self) -> Session:
        self.session = requests.Session()
        url = "https://heurist.huma-num.fr/heurist/api/login"

        body = {
            "db": self.db,
            "login": self.login,
            "password": self.password,
        }
        _ = self.session.post(url=url, data=body)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class HeuristAPIClient:
    """Client for Heurist API."""

    def __init__(self, database_name: str, login: str, password: str) -> None:
        if not database_name:
            raise ValueError("Database cannot be None.")
        if not login:
            raise ValueError("Login cannot be None.")
        if not password:
            raise ValueError("Password cannot be None.")

        self.database_name = database_name
        self.url_builder = URLBuilder(database_name=database_name)
        self.__login = login  # Private variable
        self.__password = password  # Private variable

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
        with HeuristSession(
            db=self.database_name, login=self.__login, password=self.__password
        ) as session:
            response = session.get(url, timeout=10)
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


def make_client(
    database_name: str | None = None,
    login: str | None = None,
    password: str | None = None,
) -> HeuristAPIClient:
    load_dotenv(find_dotenv())
    if not database_name:
        database_name = os.environ["DB_NAME"]
    if not login:
        login = os.environ["DB_LOGIN"]
    if not password:
        password = os.environ["DB_PASSWORD"]

    return HeuristAPIClient(database_name=database_name, login=login, password=password)
