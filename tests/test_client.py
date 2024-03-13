from heurist_api.client import HeuristAPIClient
import unittest
from pathlib import Path
from lxml import etree
import yaml

TEST_CONFIG = Path(__file__).parent.joinpath("config.yaml")


NS = "https://heuristnetwork.org"


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        with open(TEST_CONFIG) as f:
            config = yaml.safe_load(f)
            self.cookie = config["cookie"]
            self.db = config["db"]
        self.client = HeuristAPIClient(db=self.db, session_id=self.cookie)

    def test_xml_export(self):
        RECORD_TYPE = 102
        QUERY = "t:102"

        # Export the records to an HTML file
        fp = self.client.export_records(RECORD_TYPE)

        # Parse the HTML file
        tree = etree.parse(fp)

        # Confirm the query is what is expected
        query = tree.find("hml:query", namespaces={"hml": NS})
        self.assertEqual(QUERY, query.get("q"))

    def test_db_structure_export(self):
        fp = self.client.export_structure()


if __name__ == "__main__":
    unittest.main()
