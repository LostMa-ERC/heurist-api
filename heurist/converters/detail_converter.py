"""Class for converting a record's detail before the Pydantic model validation."""

from heurist.converters.date_handler import HeuristDateHandler
from heurist.converters.type_handler import HeuristDataType


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

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail.get("value", {}).get("file", {}).get("ulf_ExternalFileReference")

    @classmethod
    def enum(cls, detail: dict) -> str:
        """Extract the value of an enum field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail["termLabel"]

    @classmethod
    def geo(cls, detail: dict) -> str:
        """Extract the value of a geo field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        geo = detail["value"]["geo"]
        if geo["type"] == "p" or geo["type"] == "pl":
            return geo["wkt"]

    @classmethod
    def date(cls, detail: dict) -> list:
        """Extract the value of a date field.

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
    def resource(cls, detail: dict) -> int:
        """Extract the value of a resource field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return int(detail["value"]["id"])

    @classmethod
    def _fieldname(cls, dty_ID: int) -> str:
        """Format a name for the data field (aka "detail type", "dty").

        Args:
            detail (dict): A record's detail, which includes its DTY ID.

        Returns:
            str: A formatted label for the data field.
        """

        return f"DTY{dty_ID}"

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
