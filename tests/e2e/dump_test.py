import os
import unittest
from pathlib import Path

from dotenv import load_dotenv

from heurist.src.api_client import HeuristClient
from heurist.cli_commands.dump import dump_command


def get_test_client_env_vars() -> dict:
    load_dotenv(Path(__file__).parent.joinpath(".env"))
    db = os.environ.get("DB_NAME")
    login = os.environ.get("DB_LOGIN")
    password = os.environ.get("DB_PASSWORD")

    return {"database_name": db, "login": login, "password": password}


class DumpCommand(unittest.TestCase):
    def setUp(self):
        env_vars = get_test_client_env_vars()
        try:
            self.client = HeuristClient(**env_vars)
        except KeyError:
            self.skipTest(
                "Connection could not be established.\nCannot test client without \
                    database connection."
            )

    def test(self):
        dump_command(
            client=self.client,
            filepath=":memory:",
            record_group="My record groups",
            user=(),
            outdir=None,
        )
