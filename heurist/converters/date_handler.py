import logging
from datetime import datetime

import dateutil
import dateutil.parser
import dateutil.relativedelta

logger = logging.getLogger(__name__)


class HeuristDateHandler:
    def __init__(self) -> None:
        pass

    @classmethod
    def __call__(cls, v: str | int | list[str]) -> list[datetime]:
        if isinstance(v, list):
            d1, d2 = cls.parse(v[0]), cls.parse(v[1])
            date_list = sorted([d1, d2])
        else:
            v = str(v)
            date_list = [cls.parse(v), None]
        return date_list

    @classmethod
    def fill_out_date_str(cls, v: str | int):
        v = str(v)
        if len(v) == 4:
            v = f"{v}-01-01"
        elif "." in v:
            splits = v.split(".")
            year, smaller_than_year = splits[0], splits[1]
            if len(smaller_than_year) == 2:
                v = f"{year}-{smaller_than_year}-01"
            elif len(smaller_than_year) == 4:
                v = f"{year}-{smaller_than_year[:2]}-{smaller_than_year[2:]}"
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
