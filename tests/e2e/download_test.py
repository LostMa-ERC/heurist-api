import unittest
from pathlib import Path

import duckdb

from heurist.api.connection import HeuristConnection
from heurist.api.exceptions import MissingParameterException
from heurist.cli.load import load_command


class DownloadCommand(unittest.TestCase):
    def setUp(self):
        try:
            self.client = HeuristConnection()
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        self.database_connection_path = Path(__file__).parent.joinpath("test.db")

    def tearDown(self):
        self.database_connection_path.unlink()

    def test_database_serialization(self):
        load_command(
            client=self.client,
            duckdb_database_connection_path=self.database_connection_path,
        )

        conn = duckdb.connect(str(self.database_connection_path))
        expected = 5  # 5 non-record tables are created
        actual = len(conn.execute("show tables;").fetchall())
        self.assertGreater(actual, expected)


if __name__ == "__main__":
    unittest.main()
