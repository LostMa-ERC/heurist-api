import unittest

from heurist_api.client import make_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.record_parser import Records
from heurist_api.schemas import RelationshipMarker
from heurist_api.relationship_marker_parser import RelationshipMarkers
from heurist_api.utils import load_json
from tests import EXPORT_DIR


class RelationalTableTest(unittest.TestCase):
    record_types = [102, 103]
    validated_data = []

    def setUp(self) -> None:
        self.client = make_client()
        xml = self.client.get_structure()

        # Parse the structure
        self.parser = DBStructureParser(xml)

        for record_type in self.record_types:

            # According to the DB Parser, design a model for the record type
            model = self.parser.create_record_model(record_type=record_type)
            records = Records(model=model)

            # Collect the record type's JSON export
            json_load = load_json(client=self.client, record_id=record_type)
            data = json_load.get("heurist", {}).get("records")

            # Validate the export according to the model
            records.validate_data(data)
            self.validated_data.append(records)

    def test_list_all_record_ids(self):
        for data in self.validated_data:
            record_type = data.model.get_record_type()
            self.assertIsNotNone(record_type)
            for json_string in data.to_json_strings():
                id = json_string.get("H-ID")
                self.assertIsNotNone(id)


class RelationshipMarkerTest(unittest.TestCase):
    record_type_id = 102

    def setUp(self) -> None:
        self.client = make_client()
        self.markers = RelationshipMarkers(client=self.client)

    def test_validation(self):
        for marker in self.markers:
            self.assertIsInstance(marker, RelationshipMarker)

    def test_writing_to_json(self):
        outfile = EXPORT_DIR.joinpath("relationship_markers.json")
        self.markers.to_delimited_json(outfile=outfile)


if __name__ == "__main__":
    unittest.main()
