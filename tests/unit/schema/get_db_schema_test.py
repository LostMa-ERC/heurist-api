import unittest

from heurist.api.client import HeuristAPIClient
from heurist.api.param_manager import APIParamManager
from heurist.cli.schema import get_database_schema


class SchemaTest(unittest.TestCase):

    def setUp(self):
        params = APIParamManager(debugging=True)
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
