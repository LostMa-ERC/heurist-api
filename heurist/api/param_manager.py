"""
Parameter manager for the Heurist API Client's authentication credentials.
"""

import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from heurist.api.exceptions import MissingParameterException


class APIParamManager:
    """
    Manager for the Heurist API Client's authentication credentials.
    """

    def __init__(
        self,
        database_name: str | None = None,
        login: str | None = None,
        password: str | None = None,
        debugging: bool = False,  # Create parameters for tests' mock database
        get_env_vars: bool = True,  # Test the raising of exceptions
    ) -> None:
        """
        Parse and/or recover the parameters needed for the Heurist API client. \
            If values are not provided, try looking for them in the environment \
            variables.

        Examples:
        >>> # Set environment variables
        >>> os.environ["DB_NAME"] = "db"
        >>> os.environ["DB_LOGIN"] = "user"
        >>> os.environ["DB_PASSWORD"] = "pass"
        >>>
        >>> # Test using environment variables
        >>> params = APIParamManager()
        >>> params.database_name
        'db'
        >>> params.login
        'user'
        >>> params.password
        'pass'
        >>>
        >>> # Test for mock database
        >>> params = APIParamManager(debugging=True)
        >>> params.database_name
        'test_db'
        >>> params.login
        'test_user'
        >>> params.password
        'test_password'

        Args:
            database_name (str | None, optional): Name of the Heurist database. \
                Defaults to None.
            login (str | None, optional): Heurist user's account name. Defaults to None.
            password (str | None, optional): Heurist user's password. Defaults to None.
            debugging (bool, optional): Whether or not to use fake credentials. \
                Defaults to False.
            get_env_vars (bool, optional): Whether or not to try getting variables \
                from environment. Defaults to True.
        """

        if debugging:
            self.database_name = "test_db"
            self.login = "test_user"
            self.password = "test_password"
        else:
            self.database_name = database_name
            self.login = login
            self.password = password
            self.check_params(get_env_vars=get_env_vars)

    def check_params(
        self, get_env_vars: bool = True
    ) -> None | MissingParameterException:
        """
        Check that all the parameters are available, either provided with the class \
            instance or in the environment variables.

        Examples:
            >>> # Do not get parameters from environment variables
            >>> params = {"get_env_vars": False}
            >>> # Raise exception because database name was not provided
            >>> APIParamManager(**params)
            Traceback (most recent call last):
            ...
            heurist.api.exceptions.MissingParameterException: Missing parameter: DB_NAME
            >>> # Raise exception because login was not provided
            >>> params.update({"database_name": "test_db"})
            >>> APIParamManager(**params)
            Traceback (most recent call last):
            ...
            heurist.api.exceptions.MissingParameterException: Missing parameter: \
                DB_LOGIN
            >>> # Raise exception because password was not provided
            >>> params.update({"database_name": "test_db", "login": "test_user"})
            >>> APIParamManager(**params)
            Traceback (most recent call last):
            ...
            heurist.api.exceptions.MissingParameterException: Missing parameter: \
                DB_PASSWORD

        Raises:
            MissingParameterException: If a parameter is missing, raise an exception.
        """

        # Do not try loading environment variables if running doctest
        if get_env_vars:
            loaded_env_vars = load_dotenv(find_dotenv())
            if not loaded_env_vars:
                load_dotenv(find_dotenv(Path.cwd().joinpath(".env")))
            # Try getting parameters from environment variables
            self.database_name = os.environ.get("DB_NAME")
            self.login = os.environ.get("DB_LOGIN")
            self.password = os.environ.get("DB_PASSWORD")

        if self.database_name is None:
            raise MissingParameterException(parameter="DB_NAME")

        if self.login is None:
            raise MissingParameterException(parameter="DB_LOGIN")

        if self.password is None:
            raise MissingParameterException(parameter="DB_PASSWORD")

    @property
    def kwargs(self) -> dict:
        """
        Return the Heurist API client's authentication parameters as a dictionary.

        Examples:
        >>> vs = {"database_name": "db", "login": "user", "password": "pass", \
            "debugging": True}
        >>> params = APIParamManager(**vs)
        >>> params.kwargs
        {'database_name': 'test_db', 'login': 'test_user', 'password': 'test_password'}

        Returns:
            dict: Heurist API client parameters in key-value pairs.
        """

        return {
            "database_name": self.database_name,
            "login": self.login,
            "password": self.password,
        }
