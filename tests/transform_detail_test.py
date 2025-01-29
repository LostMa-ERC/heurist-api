from src.database.database import LoadedDatabase
from examples import DB_STRUCTURE_XML
from typing import Union
from datetime import datetime

l = [1170, {"start": 1170, "end": 1200}]

print(any(type(x) == dict for x in [1170, 1200]))
