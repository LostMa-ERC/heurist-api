from typing import Any, Optional, Dict, List
import dateutil.parser
import dateutil.relativedelta
import dateutil
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def flatten_record_detail(detail: Dict) -> Dict:
    """Transforms the Heurist detail into a key-value pair.

    Args:
        detail (Dict): Heurist detail JSON object

    Returns:
        Dict: flattened key-value
    """
    # Construct the field's name
    key = f"dty_{detail['dty_ID']}"

    # Determine the type of data in the field
    fieldtype = detail["fieldType"]

    value = detail["value"]

    # If the data is from a drop-down list (enum), get the label
    if fieldtype == "enum":
        value = detail["termLabel"]

    # If the data is geospatial, get the value
    elif fieldtype == "geo":
        geo = detail["value"]["geo"]
        if geo["type"] == "p":
            value = geo["wkt"]

    # If the data is a date, parse the range
    elif fieldtype == "date":
        handler = HeuristDateHandler()
        if (
            isinstance(value, Dict)
            and "end" in value.keys()
            and "start" in value.keys()
        ):
            end_date = value["end"]["latest"]
            start_date = value["start"]["earliest"]
            value = handler([start_date, end_date])
        elif isinstance(value, str) or isinstance(value, int):
            value = handler(value)
        else:
            value = []

    # If the data is a resource pointer, parse the id
    elif fieldtype == "resource":
        target_record_type = value["type"]
        target_record_id = value["id"]
        value = f"RecType {target_record_type} H-ID {target_record_id}"

    if not isinstance(value, Dict):
        return {key: value}


class HeuristDateHandler:
    def __init__(self) -> None:
        pass

    @classmethod
    def __call__(cls, v: str | int | List[str]) -> List[datetime]:
        if isinstance(v, List):
            d1, d2 = cls.parse(v[0]), cls.parse(v[1])
            l = sorted([d1, d2])
        else:
            v = str(v)
            l = [cls.parse(v)]
        return l

    @classmethod
    def fill_out_date_str(cls, v: str | int):
        v = str(v)
        if len(v) == 4:
            v = f"{v}-01-01"
        else:
            parts = v.split("-")
            if len(parts) == 2:
                v = f"{v}-01"
        return v

    @classmethod
    def parse(cls, d: str) -> datetime:
        v = cls.fill_out_date_str(d)
        try:
            return dateutil.parser.parse(v)
        except Exception as e:
            logger.warn(e)


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
    def to_pydantic(cls, datatype: str) -> Any:
        if datatype == cls.dropdown:
            return Optional[str]

        elif datatype == cls.numeric:
            return Optional[float]

        elif datatype == cls.single_line:
            return Optional[str]

        elif datatype == cls.multi_line:
            return Optional[str]

        elif datatype == cls.date_time:
            return List[Optional[datetime]]

        elif datatype == cls.geospatial:
            return Optional[str]

        elif datatype == cls.file_or_media_url:
            return Optional[str]

        elif datatype == cls.record_pointer:
            return Optional[str]

        elif datatype == cls.relationship_marker:
            return Optional[str]

        else:
            return Optional[str]
