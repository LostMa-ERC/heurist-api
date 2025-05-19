import unittest

from heurist.api.credentials import CredentialHandler
from heurist.cli.schema import get_database_schema


class SchemaTest(unittest.TestCase):
    def setUp(self):
        try:
            self.credentials = CredentialHandler()
        except SystemExit:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        self.debugging = True

    def test(self):
        db = get_database_schema(
            record_groups=["My record types"],
            credentials=self.credentials,
            debugging=True,
        )
        actual = len(db.pydantic_models)
        self.assertGreater(actual, 0)


if __name__ == "__main__":
    unittest.main()
