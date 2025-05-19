import unittest

import duckdb
from heurist.validators.record_validator import VALIDATION_LOG

from heurist.database.database import TransformedDatabase
from mock_data import DB_STRUCTURE_XML


class ModelingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = TransformedDatabase(
            DB_STRUCTURE_XML,
            conn=duckdb.connect(),
        )
        group_id = (
            self.db.conn.table("rtg")
            .filter("rtg_Name like 'My record types'")
            .select("rtg_ID")
            .fetchone()[0]
        )
        self.record_types = [
            t[0]
            for t in self.db.conn.table("rty")
            .filter(f"rty_RecTypeGroupID = {group_id}")
            .select("rty_ID")
            .fetchall()
        ]

    def tearDown(self):
        VALIDATION_LOG.unlink(missing_ok=True)

    def test_all_my_records(self):
        for id in self.record_types:
            r = self.db.describe_record_schema(id)
            self.assertIsNotNone(r)


if __name__ == "__main__":
    unittest.main()
