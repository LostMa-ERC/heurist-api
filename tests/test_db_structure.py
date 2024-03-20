import unittest
from pydantic import BaseModel

from tests import make_test_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.schemas.dynamic_record import create_record_model


class SchemaTest(unittest.TestCase):
    record_type_id = 105

    def setUp(self) -> None:
        self.client = make_test_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test_join_schemas(self):
        record_fields = self.parser.parse_record_field_params(self.record_type_id)
        for f in record_fields:
            self.assertIsInstance(f, BaseModel)

    def test_create_record_model(self):
        record_fields = self.parser.parse_record_field_params(self.record_type_id)
        RecordModel = create_record_model(
            name=f"rec_{self.record_type_id}", fields=record_fields
        )
        model = RecordModel()
        self.assertIsInstance(model, BaseModel)


if __name__ == "__main__":
    unittest.main()
