"""Heurist API client wrapper"""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from src.api_client.client import HeuristAPIClient


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
