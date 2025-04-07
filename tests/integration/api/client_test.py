"""
Test of the API client.
Requires a connection to a remote Heurist database.

Declare the login credentials in a .env file
"""

import unittest
from lxml import etree

from heurist.api.credentials import CredentialHandler
from heurist.api.connection import HeuristAPIConnection
from heurist.api.exceptions import AuthenticationError, MissingParameterException


TEST_RECORD_TYPE = 103
TEST_USER = 2


class ClientUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        CredentialHandler._reset_envvars()
        try:
            self.credentials = CredentialHandler()
        except MissingParameterException:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )

    def test_user_filter(self):
        """Test the API client's ability to extract records created by a \
            certain user."""

        with HeuristAPIConnection(
            db=self.credentials.get_database(),
            login=self.credentials.get_login(),
            password=self.credentials.get_password(),
        ) as client:
            try:
                records = client.get_records(
                    record_type_id=TEST_RECORD_TYPE, users=(TEST_USER,)
                )
            except AuthenticationError:
                self.skipTest(
                    "Connection could not be established.\nCannot test client without \
                        database connection."
                )

        # Confirm that every record was made by the targeted user
        for record in records:
            expected = str(TEST_USER)
            actual = record.get("rec_AddedByUGrpID")
            self.assertEqual(expected, actual)

    def test_hml_export(self):
        """Test the API client's ability to extract the database schema."""

        with HeuristAPIConnection(
            db=self.credentials.get_database(),
            login=self.credentials.get_login(),
            password=self.credentials.get_password(),
        ) as client:

            # Confirm that the client receives bytes data.
            try:
                hml_bytes = client.get_structure()
            except AuthenticationError:
                self.skipTest(
                    "Connection could not be established.\nCannot test client without \
                        database connection."
                )
            self.assertIsInstance(hml_bytes, bytes)

        # Confirm that the data is the <hml_structure> XML.
        root = etree.fromstring(hml_bytes)
        expected = "hml_structure"
        actual = root.tag
        self.assertEqual(expected, actual)

    def test_json_records(self):
        """Test the API client's ability to extract records in a JSON array."""
        with HeuristAPIConnection(
            db=self.credentials.get_database(),
            login=self.credentials.get_login(),
            password=self.credentials.get_password(),
        ) as client:
            try:
                records = client.get_records(record_type_id=TEST_RECORD_TYPE)
            except AuthenticationError:
                self.skipTest(
                    "Connection could not be established.\nCannot test client without \
                        database connection."
                )

        # Confirm that the data is a JSON array.
        self.assertIsInstance(records, list)
        self.assertIsInstance(records[0], dict)

    def test_xml_records(self):
        """Test the API client's ability to extract records in XML bytes"""

        with HeuristAPIConnection(
            db=self.credentials.get_database(),
            login=self.credentials.get_login(),
            password=self.credentials.get_password(),
        ) as client:

            # Confirm that the client receives bytes data.
            try:
                records = client.get_records(
                    record_type_id=TEST_RECORD_TYPE, form="xml"
                )
            except AuthenticationError:
                self.skipTest(
                    "Connection could not be established.\nCannot test client without \
                        database connection."
                )
        self.assertIsInstance(records, bytes)

        # Confirm that the data is a record XML.
        root = etree.fromstring(records)
        expected = r"{https://heuristnetwork.org}hml"
        actual = root.tag
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
