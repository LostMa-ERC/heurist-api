import unittest

from examples import DB_STRUCTURE_XML
from heurist.components.database.database import Database
from heurist.doc.json import convert_rty_description


class DocJSONTest(unittest.TestCase):
    def setUp(self) -> None:
        xml = DB_STRUCTURE_XML
        self.db = Database(hml_xml=xml)

    def test(self):
        # Text record type
        id = 101
        desc = self.db.describe_record_fields(id)
        d = convert_rty_description(description=desc)
        schema = d[id]["sections"]
        for section in schema:
            if section["sectionName"] == "Label Components":
                # fields in label section: preferred_name, language, literary_form
                self.assertEqual(3, len(section["fields"]))


if __name__ == "__main__":
    unittest.main()
