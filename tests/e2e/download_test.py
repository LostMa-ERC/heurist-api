import unittest

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.api.exceptions import MissingParameterException
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
        load_command(
            client=self.client,
            filepath=":memory:",
            record_group="My record groups",
            user=(),
            outdir=None,
        )


if __name__ == "__main__":
    unittest.main()
