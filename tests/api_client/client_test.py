"""
Test of the API client.
Requires a connection to a remote Heurist database.

Declare the login credentials in a .env file in the parent tests/ directory.
"""

import os
import unittest
from pathlib import Path

from dotenv import load_dotenv
from lxml import etree

from src.api_client import HeuristClient


def get_test_client_env_vars() -> dict:
    load_dotenv(Path(__file__).parent.joinpath(".env"))
    db = os.environ.get("DB_NAME")
    login = os.environ.get("DB_LOGIN")
    password = os.environ.get("DB_PASSWORD")

    return {"database_name": db, "login": login, "password": password}


TEST_RECORD_TYPE = 102
TEST_USER = 6
USER_CREATED_RECORDS = 5


class ClientUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        env_vars = get_test_client_env_vars()
        try:
            self.client = HeuristClient(**env_vars)
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without database connection."
            )

    def test_user_filter(self):
        """Test the API client's ability to extract records created by a certain user."""
        records = self.client.get_records(
            record_type_id=TEST_RECORD_TYPE, users=(TEST_USER,)
        )

        # Confirm that the number of records matches what is expected for this user in the test database.
        self.assertEqual(len(records), USER_CREATED_RECORDS)

    def test_hml_export(self):
        """Test the API client's ability to extract the database schema."""

        # Confirm that the client receives bytes data.
        hml_bytes = self.client.get_structure()
        self.assertIsInstance(hml_bytes, bytes)

        # Confirm that the data is the <hml_structure> XML.
        root = etree.fromstring(hml_bytes)
        expected = "hml_structure"
        actual = root.tag
        self.assertEqual(expected, actual)

    def test_json_records(self):
        """Test the API client's ability to extract records in a JSON array."""
        records = self.client.get_records(record_type_id=TEST_RECORD_TYPE)

        # Confirm that the data is a JSON array.
        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)

    def test_xml_records(self):
        """Test the API client's ability to extract records in XML bytes"""

        # Confirm that the client receives bytes data.
        records = self.client.get_records(record_type_id=TEST_RECORD_TYPE, form="xml")
        self.assertIsInstance(records, bytes)

        # Confirm that the data is a record XML.
        root = etree.fromstring(records)
        expected = r"{https://heuristnetwork.org}hml"
        actual = root.tag
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
