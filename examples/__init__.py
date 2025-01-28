import json
from pathlib import Path

from examples.data_types.enum import ENUM
from examples.data_types.fuzzy_date import FUZZY_DATE
from examples.data_types.media_url import MEDIA_URL
from examples.data_types.multi_line import MULTI_LINE
from examples.data_types.numeric import NUMERIC
from examples.data_types.point import POINT
from examples.data_types.polygon import POLYGON
from examples.data_types.record_pointer import RECORD_POINTER
from examples.data_types.simple_date import SIMPLE_DATE
from examples.data_types.single_line import SINGLE_LINE

DIR = Path(__file__).parent

DB_STRUCTURE_XML_FILE = DIR.joinpath("hml.xml")
RECORD_JSON_FILE = DIR.joinpath("records.json")
FUZZY_DATE_JSON_FILE = DIR.joinpath("fuzzydate_record.json")


with open(DB_STRUCTURE_XML_FILE, "rb") as f:
    DB_STRUCTURE_XML = f.read()


with open(RECORD_JSON_FILE) as f:
    r = f.read()
    RECORD_JSON = json.loads(r)


with open(FUZZY_DATE_JSON_FILE) as f:
    r = f.read()
    FUZZY_DATE_RECORD_JSON = json.loads(r)
