import os
import unittest

import pytest
from heurist.api.connection import HeuristAPIConnection
from heurist.api.credentials import CredentialHandler

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(
    IN_GITHUB_ACTIONS, reason="Do not run connection test in GitHub Actions."
)
class ConnectionWithEnvVars(unittest.TestCase):
    def setUp(self):
        """Reset environment variables"""
        CredentialHandler._reset_envvars()
        return super().setUp()

    def test_database_env_var(self):
        database = CredentialHandler(database_name=None).get_database()
        self.assertIsNotNone(database)

    def test_database_connection(self):
        credentials_from_env_vars = CredentialHandler()
        credentials_from_env_vars.test_connection()

    def test_client_request(self):
        credentials = CredentialHandler(database_name="api_dev")
        with HeuristAPIConnection(
            db=credentials.get_database(),
            login=credentials.get_login(),
            password=credentials.get_password(),
        ) as client:
            response = client.get_records(form="json", record_type_id=103)
        expected = "Symphony No. 1 in D major"
        actual = [i["rec_Title"] for i in response if i["rec_ID"] == "279"][0]
        self.assertEqual(expected, actual)

    def tearDown(self):
        """Reset environment variables"""
        CredentialHandler._reset_envvars()
        return super().tearDown()


class ConnectionWithoutEnvVars(unittest.TestCase):
    def setUp(self):
        """Reset environment variables"""
        CredentialHandler._reset_envvars()
        return super().setUp()

    def test_missing_login(self):
        with pytest.raises(SystemExit):
            CredentialHandler(login=None, debugging=True)

    def test_missing_db_name(self):
        with pytest.raises(SystemExit):
            CredentialHandler(database_name=None, debugging=True)

    def test_missing_password(self):
        with pytest.raises(SystemExit):
            CredentialHandler(password=None, debugging=True)

    def test_invalid_database_credentials(self):
        with pytest.raises(SystemExit):
            CredentialHandler(
                database_name="test_db",
                login="test_user",
                password="test_pass",
            ).test_connection()

    def tearDown(self):
        """Reset environment variables"""
        CredentialHandler._reset_envvars()
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
