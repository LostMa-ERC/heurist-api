"""Heurist API session"""

import requests
from heurist.api.client import HeuristAPIClient
from heurist.api.constants import READTIMEOUT
from heurist.api.exceptions import AuthenticationError
from requests import Session


class HeuristAPIConnection:
    def __init__(
        self,
        db: str,
        login: str,
        password: str,
        read_timeout: int = READTIMEOUT,
        post_timeout: int = 10,
    ) -> None:
        """
        Session context for a connection to the Heurist server.

        Args:
            db (str): Heurist database name.
            login (str): Username.
            password (str): User's password.
            read_timeout (int): Seconds to wait before raising a ReadTimeout.
            post_timeout (int): Seconds to wait before raising an error when \
                establishing a login connection.

        Raises:
            e: If the requests method fails, raise that exception.
            AuthenticationError: If the Heurist server returns a bad status code, \
                raise an exception.
        """

        self.db = db
        self.__login = login
        self.__password = password
        self._readtimeout = read_timeout
        self._posttimeout = post_timeout

    def __enter__(self) -> Session:
        self.session = requests.Session()
        url = "https://heurist.huma-num.fr/heurist/api/login"

        body = {
            "db": self.db,
            "login": self.__login,
            "password": self.__password,
        }
        try:
            response = self.session.post(url=url, data=body, timeout=self._posttimeout)
        except requests.exceptions.ConnectTimeout as e:
            print(
                "\nUnable to log in to Heurist Huma-Num server. \
                  Connection timed out."
            )
            raise e
        if response.status_code != 200:
            message = response.json()["message"]
            e = AuthenticationError(message)
            raise SystemExit(e)

        return HeuristAPIClient(
            database_name=self.db,
            session=self.session,
            timeout_seconds=self._readtimeout,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
