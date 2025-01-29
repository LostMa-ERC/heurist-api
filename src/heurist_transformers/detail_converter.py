"""Class for converting a record's detail before the Pydantic model validation."""

from typing import Generator

from src.heurist_transformers.date_handler import HeuristDateHandler
from src.heurist_transformers.type_handler import HeuristDataType


class RecordDetailConverter:
    """In Heurist, a record's "detail" is what is more commonly
    known as an attribute, dimension, or the value of a data field.
    """

    direct_values = ["freetext", "blocktext", "integer", "boolean", "float"]

    def __init__(self) -> None:
        pass

    @classmethod
    def file(cls, detail: dict) -> str:
        """Extract the value of a file field.

        Examples:
            >>> from examples import MEDIA_URL
            >>>
            >>>
            >>> RecordDetailConverter.file(MEDIA_URL)
            'https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail.get("value", {}).get("file", {}).get("ulf_ExternalFileReference")

    @classmethod
    def enum(cls, detail: dict) -> str:
        """Extract the value of an enum field.

        Examples:
            >>> from examples import ENUM
            >>>
            >>>
            >>> RecordDetailConverter.enum(ENUM)
            'Disease'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail["termLabel"]

    @classmethod
    def geo(cls, detail: dict) -> str:
        """Extract the value of a geo field.

        Examples:
            >>> from examples import POINT
            >>>
            >>>
            >>> RecordDetailConverter.geo(POINT)
            'POINT(2.19726563 48.57478991)'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        geo = detail["value"]["geo"]
        if geo["type"] == "p":
            return geo["wkt"]

    @classmethod
    def date(cls, detail: dict) -> list:
        """Extract the value of a date field.

        Examples:
            >>> from examples import FUZZY_DATE
            >>>
            >>>
            >>> RecordDetailConverter.date(FUZZY_DATE)
            [datetime.datetime(1180, 1, 1, 0, 0), datetime.datetime(1250, 12, 31, 0, 0)]
            >>>
            >>>
            >>> from examples import SIMPLE_DATE
            >>>
            >>>
            >>> RecordDetailConverter.date(SIMPLE_DATE)
            [datetime.datetime(2024, 3, 19, 0, 0), None]

        Args:
            detail (dict): Record's detail.

        Returns:
            list: List of one or two dates.
        """

        value = detail["value"]
        handler = HeuristDateHandler()
        if isinstance(value, dict):
            end_date = value["estMaxDate"]
            start_date = value["estMinDate"]
            value = handler([start_date, end_date])
        elif isinstance(value, str) or isinstance(value, int):
            value = handler(value)
        else:
            value = []
        return value

    @classmethod
    def resource(cls, detail: dict) -> str:
        """Extract the value of a resource field.

        Examples:
            >>> from examples import RECORD_POINTER
            >>>
            >>>
            >>> RecordDetailConverter.resource(RECORD_POINTER)
            '36'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        value = detail["value"]
        return value["id"]

    @classmethod
    def _fieldname(cls, dty_ID: int, temp: bool = False) -> str:
        """Format a name for the data field (aka "detail type", "dty").

        Args:
            detail (dict): A record's detail, which includes its DTY ID.
            temp (bool, optional): Whether or not the fieldname will represent a temporal object (JSON dict). Defaults to False.

        Returns:
            str: A formatted label for the data field.
        """

        suffix = ""
        if temp:
            suffix = "_TEMPORAL"
        return f"DTY{dty_ID}{suffix}"

    @classmethod
    def _convert_value(cls, detail: dict) -> str | int | list | None:
        """Based on the data type, convert the record's nested detail to a flat value.

        Args:
            detail (dict): One of the record's details (data fields).

        Returns:
            str | int | list | None: Flattened value of the data field.
        """

        fieldtype = HeuristDataType.from_json_record(detail)

        if any(ft in fieldtype for ft in cls.direct_values):
            return detail["value"]

        elif fieldtype == "date":
            return cls.date(detail)

        elif fieldtype == "enum":
            return cls.enum(detail)

        elif fieldtype == "file":
            return cls.file(detail)

        elif fieldtype == "geo":
            return cls.geo(detail)

        elif fieldtype == "resource":
            return cls.resource(detail)
