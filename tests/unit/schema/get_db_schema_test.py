import unittest

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.cli.schema import get_database_schema
from heurist.api.exceptions import MissingParameterException


class SchemaTest(unittest.TestCase):

    def setUp(self):
        try:
            params = APIParamManager(debugging=True)
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )
        self.client = HeuristAPIClient(**params.kwargs)
        self.debugging = True

    def test(self):
        db = get_database_schema(
            record_groups=["My record types"],
            client=self.client,
            debugging=True,
        )
        actual = len(db.pydantic_models)
        self.assertGreater(actual, 0)


if __name__ == "__main__":
    unittest.main()
