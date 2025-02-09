"""Heurist API session"""

import requests
from requests import Session


class HeuristRequestSession:
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
        try:
            _ = self.session.post(url=url, data=body)
        except Exception as e:
            print(
                "\nUnable to login to Heurist Huma-Num server. \
                  Connection timed out."
            )
            raise e
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
