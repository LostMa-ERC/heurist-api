"""Class for converting a record's detail before the Pydantic model validation."""

from datetime import datetime

from heurist.converters.date_handler import HeuristDateHandler
from heurist.converters.type_handler import HeuristDataType
from heurist.models.date import TemporalObject


class RecordDetailConverter:
    """
    In Heurist, a record's "detail" is what is more commonly known as an attribute, \
        dimension, or the value of a data field.

    This class features methods to extract the key value from Heurist's JSON \
        formatting for all data types in Heurist's system.
    """

    direct_values = ["freetext", "blocktext", "integer", "boolean", "float"]

    def __init__(self) -> None:
        pass

    @classmethod
    def file(cls, detail: dict) -> str:
        """
        Extract the value of a file field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail.get("value", {}).get("file", {}).get("ulf_ExternalFileReference")

    @classmethod
    def enum(cls, detail: dict) -> str:
        """
        Extract the value of an enum field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail["termLabel"]

    @classmethod
    def geo(cls, detail: dict) -> str:
        """
        Extract the value of a geo field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        geo = detail["value"]["geo"]
        if geo["type"] == "p" or geo["type"] == "pl":
            return geo["wkt"]

    @classmethod
    def date(cls, detail: dict) -> list[datetime | None]:
        """
        Extract the the earliest and latest dates from a date field.

        Args:
            detail (dict): Record's detail.

        Returns:
            list[datetime]: Earliest and latest dates from detail.
        """

        value = detail["value"]
        handler = HeuristDateHandler()
        if isinstance(value, dict):
            end_date = value["estMaxDate"]
            start_date = value["estMinDate"]
            value = handler.list_min_max([start_date, end_date])
        elif isinstance(value, str) or isinstance(value, int):
            value = handler.list_min_max(value)
        else:
            value = []
        return value

    @classmethod
    def resource(cls, detail: dict) -> int:
        """
        Extract the value of a resource (foreign key) field.

        Args:
            detail (dict): Record's detail.

        Returns:
            int: Heurist ID of the referenced record.
        """

        return int(detail["value"]["id"])

    @classmethod
    def _fieldname(cls, dty_ID: int) -> str:
        """
        Format a name for the data field (aka "detail type", "dty").

        Args:
            dty_ID (int): The ID of the detail type.

        Returns:
            str: A formatted label for the data field.
        """

        return f"DTY{dty_ID}"

    @classmethod
    def temporal(cls, detail: dict) -> dict | None:
        if isinstance(detail.get("value"), dict):
            model = TemporalObject.model_validate(detail["value"])
            return model.model_dump(by_alias=True)

    @classmethod
    def _convert_value(cls, detail: dict) -> str | int | list | None:
        """
        Based on the data type, convert the record's nested detail to a flat value.

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
