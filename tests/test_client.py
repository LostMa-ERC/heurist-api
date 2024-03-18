import unittest
from lxml import etree
import re
import json

from tests import make_test_client
from heurist_api.constants import NAMESPACE


class APITest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = make_test_client()

    def test_xml_record_export(self):
        RECORD_TYPE = 100

        # Get all the records in XML format
        xml = self.client.get_records(RECORD_TYPE)

        # Confirm the test client correctly connected
        self.assertIsNotNone(xml, msg="Client did not connect to the database.")

        if xml:
            # Parse the results' query
            parser = etree.XMLParser(ns_clean=True)
            xml_root = etree.fromstring(xml, parser)
            query_string = xml_root.find("hml:query", namespaces=NAMESPACE).get("q")
            record_type_id = re.search(r"(\d+)", query_string).group(0)

            # Confirm the queried result type ID
            self.assertEqual(RECORD_TYPE, int(record_type_id))

    def test_json_record_export(self):
        RECORD_TYPE = 100

        # Get all the records in JSON format
        json_results = self.client.get_records(RECORD_TYPE, form="json")

        # Confirm the test client correctly connected
        self.assertIsNotNone(
            json_results, msg="Client did not connect to the database."
        )

        if json_results:
            # Parse the results' database name
            json_string = json_results.decode("utf-8")
            d = json.loads(json_string)
            database_in_query_result = d["heurist"]["database"]["db"]

            # Confirm the queried database name
            self.assertEqual(database_in_query_result, self.client.database_name)

    def test_xml_structure_export(self):
        # Get structure in XML format
        xml = self.client.get_structure()

        # Confirm the test client correctly connected
        self.assertIsNotNone(xml, msg="Client did not connect to the database.")

        if xml:
            # Parse the results' database name
            parser = etree.XMLParser(ns_clean=True)
            xml_root = etree.fromstring(xml, parser)
            database_name = xml_root.find("HeuristDBName").text

            # Confirm the queried database name
            self.assertEqual(database_name, self.client.database_name)


if __name__ == "__main__":
    unittest.main()
