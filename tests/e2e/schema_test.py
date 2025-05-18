import csv
import json
import unittest
from pathlib import Path

from heurist.api.credentials import CredentialHandler
from heurist.cli.schema import schema_command
from heurist.validators.record_validator import VALIDATION_LOG


class OnlineSchemaCommand(unittest.TestCase):
    tempdir = Path(__file__).parent.joinpath("temp")
    tempfile_json = tempdir.joinpath("recordTypes.json")

    def setUp(self):
        self.tempdir.mkdir(exist_ok=True)
        try:
            self.credentials = CredentialHandler()
        except SystemExit:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )

    def tearDown(self):
        for f in self.tempdir.iterdir():
            f.unlink(missing_ok=True)
        self.tempdir.rmdir()
        VALIDATION_LOG.unlink(missing_ok=True)
        return super().tearDown()

    def json(self):
        _ = schema_command(
            credentials=self.credentials,
            record_group=["My record types"],
            outdir=self.tempdir,
            output_type="json",
            debugging=True,
        )
        with open(self.tempfile_json) as f:
            data = json.load(f)
        actual = len(data["items"])
        self.assertGreater(actual, 0)

    def csv(self):
        _ = schema_command(
            credentials=self.credentials,
            record_group=["My record types"],
            outdir=self.tempdir,
            output_type="csv",
            debugging=True,
        )
        for file in self.tempdir.iterdir():
            with open(file, mode="r") as f:
                reader = csv.DictReader(f)
                row_count = len([_ for r in reader])
                self.assertGreater(row_count, 0)


if __name__ == "__main__":
    unittest.main()
