import unittest

from heurist_api.client import make_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.record_parser import Records
from heurist_api.utils import load_json

from tests import EXPORT_DIR


class RecordModelTest(unittest.TestCase):
    record_type_id = 103

    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

    def test_record_type_in_model_name(self):
        model = self.parser.create_record_model(record_type=self.record_type_id)
        records = Records(model=model)
        record_type_in_name = records.model.get_record_type()
        self.assertEqual(record_type_in_name, str(self.record_type_id))

    def test_data_validation(self):
        # According to the DB Parser, design a model for the record type
        model = self.parser.create_record_model(record_type=self.record_type_id)
        records = Records(model=model)

        # Collect the record type's JSON export
        json_load = load_json(client=self.client, record_id=self.record_type_id)
        data = json_load.get("heurist", {}).get("records")

        # Validate the export according to the model
        records.validate_data(data)

        # Confirm all valid records were converted into data models
        valid_data = [d for d in data if d["rec_RecTypeID"] == str(self.record_type_id)]
        self.assertEqual(len(records), len(valid_data))


class ModelSerializationTest(unittest.TestCase):
    record_type_id = 101

    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

        # According to the DB Parser, design a model for the record type
        model = self.parser.create_record_model(record_type=self.record_type_id)
        self.records = Records(model=model)

        # Collect the record type's JSON export
        json_load = load_json(client=self.client, record_id=self.record_type_id)
        data = json_load.get("heurist", {}).get("records")

        # Validate the export according to the model
        self.records.validate_data(data)

    def test_writing_to_csv(self):
        outfile = EXPORT_DIR.joinpath("records.csv")
        self.records.to_csv(outfile=outfile)

    def test_writing_to_json(self):
        outfile = EXPORT_DIR.joinpath("records.json")
        self.records.to_delimited_json(outfile=outfile)


if __name__ == "__main__":
    unittest.main()
