import unittest
import json

from tests import make_test_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.record_parser import Records

from tests import EXPORT_DIR


class SchemaTest(unittest.TestCase):
    record_type_id = 101

    def setUp(self) -> None:
        self.client = make_test_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test(self):
        # Set up a model for the record
        record_models = Records(parser=self.parser, record_type_id=self.record_type_id)

        # Collect the record's JSON export
        json_bytes = self.client.get_records(self.record_type_id, form="json")
        json_string = json_bytes.decode("utf-8")
        json_load = json.loads(json_string)

        # Modelize each record
        records = json_load.get("heurist", {}).get("records")
        for record in records:
            record_models(record)

        # Confirm all the records were converted into data models
        self.assertEqual(len(record_models.data), len(records))

        record_models.to_delimited_json(EXPORT_DIR.joinpath("records.json"))


if __name__ == "__main__":
    unittest.main()
