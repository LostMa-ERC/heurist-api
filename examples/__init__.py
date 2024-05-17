import json
from pathlib import Path

DIR = Path(__file__).parent

DB_STRUCTURE_XML_FILE = DIR.joinpath("hml.xml")
RECORD_JSON_FILE = DIR.joinpath("records.json")

with open(DB_STRUCTURE_XML_FILE, "rb") as f:
    DB_STRUCTURE_XML = f.read()

with open(RECORD_JSON_FILE) as f:
    r = f.read()
    RECORD_JSON = json.loads(r)
