import unittest
from pydantic import BaseModel

from heurist_api.client import make_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.schemas import RecordBaseModel
from heurist_api.utils import mock_data


class DBParserTest(unittest.TestCase):
    record_type_id = 105

    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test_join_schemas(self):
        record_fields = self.parser.parse_record_field_params(self.record_type_id)
        for f in record_fields:
            self.assertIsInstance(f, BaseModel)

    def test_create_record_model(self):
        model = self.parser.create_record_model(self.record_type_id)
        self.assertIsInstance(model(**mock_data), RecordBaseModel)


if __name__ == "__main__":
    unittest.main()
