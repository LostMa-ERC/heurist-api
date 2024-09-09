import unittest

from examples import DB_STRUCTURE_XML, RECORD_JSON, FUZZY_DATE_RECORD_JSON
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


class DatabaseDateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database(DB_STRUCTURE_XML)
        self.rectype = 106
        self.records = FUZZY_DATE_RECORD_JSON

    def test(self):
        table = self.db.insert_records(
            record_type_id=self.rectype, records=self.records
        )
        cs = [c for c in table.columns if "date" in c]
        print(table.select(*cs))


if __name__ == "__main__":
    unittest.main()
