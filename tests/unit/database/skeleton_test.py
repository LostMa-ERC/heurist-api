import unittest

from heurist.database.basedb import HeuristDatabase

from mock_data import DB_STRUCTURE_XML


class DuckBaseTest(unittest.TestCase):
    def test(self):
        """Test should show that the 5 basic data models from the HML XML
        were converted to SQL tables."""

        self.db = HeuristDatabase(hml_xml=DB_STRUCTURE_XML)
        rel = self.db.conn.sql("show tables")
        self.assertEqual(len(rel), 5)


if __name__ == "__main__":
    unittest.main()
