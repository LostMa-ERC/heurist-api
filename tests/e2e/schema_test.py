import unittest

from pathlib import Path

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.cli.schema import schema_command


class SchemaCommand(unittest.TestCase):
    tempfile_json = Path(__file__).parent.joinpath("temp.json")
    tempdir_csv = Path(__file__).parent.joinpath("temp")

    def setUp(self):
        self.tempdir_csv.mkdir(exist_ok=False)
        params = APIParamManager()
        try:
            self.client = HeuristAPIClient(**params.kwargs)
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )

    def tearDown(self):
        self.tempfile_json.unlink(missing_ok=True)
        for f in self.tempdir_csv.iterdir():
            f.unlink(missing_ok=True)
        self.tempdir_csv.rmdir()
        return super().tearDown()

    def test_json(self):
        schema_command(
            client=self.client,
            testing=True,
            record_group="My record groups",
            outdir=None,
            output_type="json",
        )

    def test_csv(self):
        schema_command(
            client=self.client,
            testing=True,
            record_group="My record groups",
            outdir=self.tempdir_csv,
            output_type="csv",
        )


if __name__ == "__main__":
    unittest.main()
