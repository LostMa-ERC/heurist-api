import unittest

from examples import DB_STRUCTURE_XML
from heurist.components.database.database import Database
from heurist.doc.html import Doc


class DocHTMLTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database(hml_xml=DB_STRUCTURE_XML)
        group_id = 23
        self.record_name_index = {
            t[0]: t[1]
            for t in self.db.conn.table("rty")
            .select("rty_ID, rty_Name")
            .order("rty_Name")
            .fetchall()
        }
        self.record_types = [
            t[0]
            for t in self.db.conn.table("rty")
            .filter(f"rty_RecTypeGroupID = {group_id}")
            .select("rty_ID, rty_Name")
            .order("rty_Name")
            .fetchall()
        ]

    @unittest.skip("")
    def test_html_base(self):
        doc = Doc()
        self.assertIsNone(doc.indented_html)

    def test_html_output(self):
        doc = Doc(
            record_name_index=self.record_name_index, present_records=self.record_types
        )
        for rty in self.record_types:
            rel = self.db.describe_record_fields(rty_ID=rty)
            doc.add_record(rel)


if __name__ == "__main__":
    unittest.main()
