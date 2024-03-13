from heurist_api.constants import EXPORT, DB_STRUCTURE
import unittest


class PathTest(unittest.TestCase):
    db = "jbcamps_gestes"

    def test_record_export_path(self):
        composed_path = EXPORT % (102, self.db)
        static_path = "https://heurist.huma-num.fr/heurist/export/xml/flathml.php?q=t%3A102&a=1&db=jbcamps_gestes&depth=all&linkmode=direct"
        self.assertEqual(composed_path, static_path)

    def test_db_structure_path(self):
        composed_path = DB_STRUCTURE % (self.db)
        static_path = "https://heurist.huma-num.fr/heurist/hserv/structure/export/getDBStructureAsXML.php?db=jbcamps_gestes&ll=H6Default"
        self.assertEqual(composed_path, static_path)


if __name__ == "__main__":
    unittest.main()
