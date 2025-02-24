import unittest

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.cli.load import load_command


class DumpCommand(unittest.TestCase):
    def setUp(self):
        params = APIParamManager()
        try:
            self.client = HeuristAPIClient(**params.kwargs)
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )

    def test(self):
        load_command(
            client=self.client,
            filepath=":memory:",
            record_group="My record groups",
            user=(),
            outdir=None,
        )
