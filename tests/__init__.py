from pathlib import Path
import yaml

from heurist_api.client import HeuristAPIClient

TEST_CONFIG = Path(__file__).parent.joinpath("config.yaml")

EXPORT_DIR = Path(__file__).parent.joinpath("export")
EXPORT_DIR.mkdir(exist_ok=True)


def make_test_client() -> HeuristAPIClient:
    with open(TEST_CONFIG) as f:
        config = yaml.safe_load(f)
        login = config["login"]
        password = config["password"]
        db = config["db"]
    return HeuristAPIClient(database_name=db, login=login, password=password)
