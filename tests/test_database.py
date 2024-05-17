import unittest

from examples import DB_STRUCTURE_XML, RECORD_JSON
from heurist.components.database.database import Database


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database(DB_STRUCTURE_XML)
        self.rectype = 101
        self.records = RECORD_JSON["heurist"]["records"]

    def test(self):
        table = self.db.insert_records(
            record_type_id=self.rectype, records=self.records
        )
        total = table.count("*").fetchone()[0]
        self.assertEqual(total, 278)


if __name__ == "__main__":
    unittest.main()
