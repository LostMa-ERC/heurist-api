import unittest

import duckdb

from heurist import TABLES_LOG, DATABASE_LOG

from heurist.examples import DB_STRUCTURE_XML
from heurist.src.database import LoadedDatabase


class ModelingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = LoadedDatabase(
            DB_STRUCTURE_XML,
            save_structure=True,
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
        TABLES_LOG.unlink(missing_ok=True)
        DATABASE_LOG.unlink(missing_ok=True)

    def test_all_my_records(self):
        for id in self.record_types:
            r = self.db.describe_record_fields(id)
            self.assertIsNotNone(r)


if __name__ == "__main__":
    unittest.main()
