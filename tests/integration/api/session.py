import unittest

from heurist.api.session import HeuristRequestSession
from heurist.api.param_manager import APIParamManager
from heurist.api.exceptions import AuthenticationError


class SesssionTest(unittest.TestCase):
    def test_good_authentication(self) -> None:
        params = APIParamManager()
        try:
            session = HeuristRequestSession(
                db=params.database_name,
                login=params.login,
                password=params.password,
            )
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        with session:
            pass

    def test_bad_authentication(self):
        params = APIParamManager(debugging=True)
        try:
            session = HeuristRequestSession(
                db=params.database_name,
                login=params.login,
                password=params.password,
            )
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        with self.assertRaises(AuthenticationError):
            with session:
                pass


if __name__ == "__main__":
    unittest.main()
