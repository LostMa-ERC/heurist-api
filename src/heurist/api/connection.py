"""Heurist API session"""

import requests
from heurist.api.client import HeuristAPIClient
from heurist.api.constants import READTIMEOUT
from heurist.api.exceptions import AuthenticationError


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
            requests.exceptions.RequestException:
                If the HTTP request fails.
            requests.exceptions.HTTPError:
                If the Heurist server returns a 5xx status code.
            AuthenticationError:
                If the Heurist server returns an unsuccessful status code below 500.
        """

        self.db = db
        self.__login = login
        self.__password = password
        self._readtimeout = read_timeout
        self._posttimeout = post_timeout
        self.session: requests.Session | None = None

    def __enter__(self) -> HeuristAPIClient:
        self.session = requests.Session()
        url = "https://heurist.huma-num.fr/heurist/hserv/controller/usr_info.php"

        body = {
            "db": self.db,
            "username": self.__login,
            "password": self.__password,
            "session_type": "remember",
            "a": "login",
        }
        try:
            response = self.session.post(
                url=url,
                data=body,
                timeout=self._posttimeout,
            )
            response.raise_for_status()
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                raise AuthenticationError(
                    "Heurist returned an invalid authentication response."
                ) from e

            if data.get("status") != "ok":
                raise AuthenticationError(
                    data.get("message", "Heurist authentication failed.")
                )

            return HeuristAPIClient(
                database_name=self.db,
                session=self.session,
                timeout_seconds=self._readtimeout,
            )
        except Exception:
            self.session.close()
            self.session = None
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.session is not None:
            self.session.close()
            self.session = None