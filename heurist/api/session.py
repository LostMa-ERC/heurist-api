"""Heurist API session"""

import requests
from requests import Session

from heurist.api.exceptions import AuthenticationError


class HeuristRequestSession:
    def __init__(self, db: str, login: str, password: str) -> None:
        """
        Session context for a connection to the Heurist server.

        Args:
            db (str): Heurist database name.
            login (str): Username.
            password (str): User's password.

        Raises:
            e: If the requests method fails, raise that exception.
            AuthenticationError: If the Heurist server returns a bad status code, \
                raise an exception.
        """

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
        try:
            response = self.session.post(url=url, data=body)
        except Exception as e:
            print(
                "\nUnable to login to Heurist Huma-Num server. \
                  Connection timed out."
            )
            raise e
        if response.status_code != 200:
            message = response.json()["message"]
            raise AuthenticationError(message)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
