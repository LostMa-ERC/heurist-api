import unittest

from heurist.validators.record_validator import VALIDATION_LOG

from heurist.database.database import TransformedDatabase
from mock_data import DB_STRUCTURE_XML, RECORD_JSON


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = TransformedDatabase(DB_STRUCTURE_XML)
        self.rectype = 103  # Story
        self.extracted_records = RECORD_JSON["heurist"]["records"]

    def tearDown(self):
        VALIDATION_LOG.unlink(missing_ok=True)

    def test(self):
        # Load the extracted records into the database
        rel = self.db.insert_records(
            records=self.extracted_records,
            record_type_id=self.rectype,
        )

        # Fetch the loaded records
        loaded_records = rel.fetchall()

        # Convert 1 of the records to a dictionary
        d = {k: v for k, v in zip(rel.columns, loaded_records[0])}

        # Confirm that the converted record's Heurist ID (H-ID) is an integer
        self.assertIsInstance(d["H-ID"], int)


if __name__ == "__main__":
    unittest.main()
