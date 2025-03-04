import os
from dotenv import find_dotenv, load_dotenv
from heurist.api.client import HeuristAPIClient, HeuristRequestSession
from heurist.api.exceptions import MissingParameterException, AuthenticationError


class HeuristConnection(HeuristAPIClient):
    def __init__(
        self,
        database_name: str | None = None,
        login: str | None = None,
        password: str | None = None,
        debugging: bool = False,
    ):
        # Affirm all the necessary parameters for a connection
        loaded_dn_name = self.load_database(database_name)
        loaded_login = self.load_login(login)
        loaded_password = self.load_password(password)

        # Test the connection
        if not debugging:
            self.test_connection(
                db=loaded_dn_name,
                login=loaded_login,
                password=loaded_password,
            )

        # If the connection test did not raise an error,
        # create an instance of the Heurist API client
        super().__init__(
            database_name=self.load_database(db_name=loaded_dn_name),
            login=self.load_login(login=loaded_login),
            password=self.load_password(password=loaded_password),
        )

    @classmethod
    def test_connection(
        cls,
        db: str,
        login: str,
        password: str,
    ) -> bool | AuthenticationError:
        with HeuristRequestSession(db=db, login=login, password=password) as _:
            return True

    @staticmethod
    def load_param(
        var: str | None,
        key: str,
        param: str,
        debugging: bool = False,
    ) -> str | MissingParameterException:
        if not var and not debugging:
            load_dotenv(find_dotenv())
            var = os.environ.get(key)
        if not var:
            raise MissingParameterException(parameter=param)
        return var

    @classmethod
    def load_database(
        cls,
        db_name: str | None,
        debugging: bool = False,
    ) -> str | MissingParameterException:
        return cls.load_param(
            var=db_name,
            key="DB_NAME",
            param="database",
            debugging=debugging,
        )

    @classmethod
    def load_login(
        cls,
        login: str | None,
        debugging: bool = False,
    ) -> str | MissingParameterException:
        return cls.load_param(
            var=login,
            key="DB_LOGIN",
            param="login",
            debugging=debugging,
        )

    @classmethod
    def load_password(
        cls,
        password: str | None,
        debugging: bool = False,
    ) -> str | MissingParameterException:
        return cls.load_param(
            var=password,
            key="DB_PASSWORD",
            param="password",
            debugging=debugging,
        )
