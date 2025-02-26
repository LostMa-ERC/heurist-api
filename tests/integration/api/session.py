import unittest

from heurist.api.session import HeuristRequestSession
from heurist.api.param_manager import APIParamManager
from heurist.api.exceptions import AuthenticationError, MissingParameterException


class SesssionTest(unittest.TestCase):
    def test_good_authentication(self) -> None:
        try:
            params = APIParamManager()
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        session = HeuristRequestSession(
            db=params.database_name,
            login=params.login,
            password=params.password,
        )
        with session:
            pass

    def test_bad_authentication(self):
        try:
            params = APIParamManager(debugging=True)
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        session = HeuristRequestSession(
            db=params.database_name,
            login=params.login,
            password=params.password,
        )
        with self.assertRaises(AuthenticationError):
            with session:
                pass


if __name__ == "__main__":
    unittest.main()
