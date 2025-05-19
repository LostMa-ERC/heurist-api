import os

from dotenv import find_dotenv, load_dotenv
from heurist.api.connection import HeuristAPIConnection
from heurist.api.exceptions import MissingParameterException


class CredentialHandler:
    env_file = find_dotenv()
    db_key = "DB_NAME"
    login_key = "DB_LOGIN"
    password_key = "DB_PASSWORD"

    def __init__(
        self,
        database_name: str | None = None,
        login: str | None = None,
        password: str | None = None,
        debugging: bool = False,
    ):
        if not debugging:
            load_dotenv(self.env_file)

        params = [
            (self.db_key, database_name),
            (self.login_key, login),
            (self.password_key, password),
        ]

        # Set all the secret variables in the environment
        for key, var in params:
            if var:
                self.set_var(key=key, var=var)
            # Confirm that the environment variable is set
            v = self.get_var(key=key)
            if not v or v == "":
                e = MissingParameterException(parameter=key, env_file=self.env_file)
                raise SystemExit(e)

    def test_connection(self) -> None:
        with HeuristAPIConnection(
            db=self.get_database(), login=self.get_login(), password=self.get_password()
        ) as _:
            pass

    @classmethod
    def _reset_envvars(cls) -> None:
        keys = [cls.db_key, cls.login_key, cls.password_key]
        for key in keys:
            if os.environ.get(key):
                os.environ.pop(key)

    @classmethod
    def set_var(cls, key: str, var: str) -> None:
        os.environ[key] = var

    @classmethod
    def get_var(cls, key: str) -> str | KeyError:
        return os.getenv(key)

    @classmethod
    def get_database(cls) -> str:
        return cls.get_var(key="DB_NAME")

    @classmethod
    def get_login(cls) -> str:
        return cls.get_var(key="DB_LOGIN")

    @classmethod
    def get_password(cls) -> str:
        return cls.get_var(key="DB_PASSWORD")
