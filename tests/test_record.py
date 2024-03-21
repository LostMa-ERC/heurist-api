import unittest

from heurist_api.client import make_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.record_parser import Records
from heurist_api.utils import load_json

from tests import EXPORT_DIR


class RecordModelTest(unittest.TestCase):
    record_type_id = 101

    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test(self):
        # According to the DB Parser, design a model for the record type
        model = self.parser.create_record_model(record_type=self.record_type_id)
        records = Records(model=model)

        # Collect the record type's JSON export
        json_load = load_json(client=self.client, record_id=self.record_type_id)
        data = json_load.get("heurist", {}).get("records")

        # Validate the export according to the model
        records.validate_data(data)

        # Confirm all the records were converted into data models
        self.assertEqual(len(records), len(data))

        # Test serialization of Json
        json_export = EXPORT_DIR.joinpath("records.json")
        records.to_delimited_json(json_export)

        # Test serialization of CSV
        csv_export = EXPORT_DIR.joinpath("records.csv")
        records.to_csv(outfile=csv_export)


if __name__ == "__main__":
    unittest.main()
