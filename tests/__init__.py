from pathlib import Path


TEST_CONFIG = Path(__file__).parent.joinpath("config.yaml")

EXPORT_DIR = Path(__file__).parent.joinpath("export")
EXPORT_DIR.mkdir(exist_ok=True)
