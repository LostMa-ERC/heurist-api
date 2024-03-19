import unittest
from pydantic import BaseModel

from tests import make_test_client
from heurist_api.db_structure_parser import DBStructureParser


class SchemaTest(unittest.TestCase):
    record_type_id = 105

    def setUp(self) -> None:
        self.client = make_test_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test_conversion(self):
        fields = self.parser.parse_record_field_params(self.record_type_id)
        for f in fields:
            self.assertIsInstance(f, BaseModel)


if __name__ == "__main__":
    unittest.main()
