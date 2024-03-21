from typing import Any, List, Optional
import dateutil.parser
from dataclasses import dataclass
from pydantic.functional_validators import BeforeValidator, AfterValidator
from datetime import datetime


def check_datetime(v):
    try:
        dateutil.parser.parse(v)
    except Exception as e:
        print("\n\n~~~~FAIL~~~~\n")
        return None
    else:
        return v


@dataclass
class HeuristDataType:
    dropdown = "enum"
    numeric = "float"
    single_line = "freetext"
    multi_line = "blocktext"
    date_time = "date"
    geospatial = "geo"
    file_or_media_url = "file"
    record_pointer = "resource"
    relationship_marker = "relmarker"

    @classmethod
    def to_duckdb(cls, datatype: str) -> str:
        if datatype == cls.dropdown:
            return "VARCHAR"

        elif datatype == cls.numeric:
            return "DOUBLE"

        elif datatype == cls.single_line:
            return "VARCHAR"

        elif datatype == cls.multi_line:
            return "VARCHAR"

        elif datatype == cls.date_time:
            return "DATE"

        elif datatype == cls.geospatial:
            return "VARCHAR"

        elif datatype == cls.file_or_media_url:
            return "VARCHAR"

        elif datatype == cls.record_pointer:
            return "BIGINT"

        elif datatype == cls.relationship_marker:
            return "VARCHAR"

        else:
            return "VARCHAR"

    @classmethod
    def to_pydantic(cls, datatype: str) -> Any:
        if datatype == cls.dropdown:
            # return "Optional[List[str]]"
            return Optional[str], None

        elif datatype == cls.numeric:
            # return "Optional[float]"
            return Optional[float], BeforeValidator(check_datetime)

        elif datatype == cls.single_line:
            # return "Optional[str]"
            return Optional[str], None

        elif datatype == cls.multi_line:
            # return "Optional[str]"
            return Optional[str], None

        elif datatype == cls.date_time:
            # return "Optional[datetime]"
            return Optional[datetime], None

        elif datatype == cls.geospatial:
            # return "Optional[str]"
            return Optional[str], None

        elif datatype == cls.file_or_media_url:
            # return "Optional[str]"
            return Optional[str], None

        elif datatype == cls.record_pointer:
            # return "Optional[int]"
            return Optional[int], None

        elif datatype == cls.relationship_marker:
            # return "Optional[str]"
            return Optional[str], None

        else:
            # return "Optional[str]"
            return Optional[str], None
