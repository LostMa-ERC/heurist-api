import unittest
import json

from tests import make_test_client
from heurist_api.db_structure_parser import DBStructureParser


class SchemaTest(unittest.TestCase):
    record_type_id = 105

    def setUp(self) -> None:
        self.client = make_test_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test(self):
        # Set up a model for the record
        model = self.parser.create_record_model(record_type=self.record_type_id)

        # Collect the record's JSON export
        json_bytes = self.client.get_records(self.record_type_id, form="json")
        json_string = json_bytes.decode("utf-8")
        json_load = json.loads(json_string)

        # Modelize each record
        models = []
        records = json_load.get("heurist", {}).get("records")
        for record in records:
            models.append(model(**record))

        # Confirm all the records were converted into data models
        self.assertEqual(len(models), len(records))


if __name__ == "__main__":
    unittest.main()
