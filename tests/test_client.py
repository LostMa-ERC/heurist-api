import unittest

from heurist.client import HeuristClient


class ClientUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = HeuristClient()

    def test_user_filter(self):
        records = self.client.get_records(record_type_id=102, users=(6,))
        self.assertEqual(len(records), 11)

    def test_hml_export(self):
        hml_bytes = self.client.get_structure()
        self.assertIsInstance(hml_bytes, bytes)

    def test_json_records(self):
        records = self.client.get_records(record_type_id=101)
        self.assertGreater(len(records), 2)

    def test_xml_records(self):
        records = self.client.get_records(record_type_id=101, form="xml")
        self.assertIsInstance(records, bytes)

    def test_relmarker_records(self):
        records = self.client.get_relationship_markers(form="json")
        self.assertEqual(len(records), 0)


if __name__ == "__main__":
    unittest.main()
