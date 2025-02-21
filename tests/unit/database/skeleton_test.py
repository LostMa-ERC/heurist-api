import unittest

from heurist.examples import DB_STRUCTURE_XML
from heurist.src.database.skeleton import DatabaseSkeleton


class DuckBaseTest(unittest.TestCase):

    def test(self):
        """Test should show that the 5 basic data models from the HML XML
        were converted to SQL tables."""

        self.db = DatabaseSkeleton(hml_xml=DB_STRUCTURE_XML)
        rel = self.db.conn.sql("show tables")
        self.assertEqual(len(rel), 5)


if __name__ == "__main__":
    unittest.main()
