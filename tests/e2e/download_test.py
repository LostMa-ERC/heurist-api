import unittest

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.api.exceptions import AuthenticationError, MissingParameterException
from heurist.cli.load import load_command


class DownloadCommand(unittest.TestCase):
    def setUp(self):
        try:
            params = APIParamManager()
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        self.client = HeuristAPIClient(**params.kwargs)

    def test(self):
        try:
            load_command(
                client=self.client,
                duckdb_database_connection_path=":memory:",
                record_group="My record groups",
                user=(),
                outdir=None,
            )
        except AuthenticationError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )


if __name__ == "__main__":
    unittest.main()
