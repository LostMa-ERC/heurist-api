"""Dataclass to organize and convert the data type of a Record's detail."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class FieldType:
    """Organize and convert the data types of a Record's detail."""

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
    def to_sql(cls, datatype: str) -> str:
        """
        Convert a Heurist data type label (i.e. "enum") to an SQL equivalent.

        Args:
            datatype (str): Heurist data type.

        Returns:
            str: SQL data type.
        """

        if datatype == cls.numeric:
            return "FLOAT"
        elif datatype == cls.date_time:
            return "DATE[2]"
        elif datatype == cls.record_pointer or datatype == cls.relationship_marker:
            return "INTEGER"
        elif datatype == cls.dropdown:
            return "VARCHAR"
        else:
            return "TEXT"

    @classmethod
    def from_detail(cls, detail: dict) -> str:
        """Extract the field type from a record's detail.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Field type name.
        """

        return detail["fieldType"]

    @classmethod
    def to_pydantic(cls, datatype: str) -> Any:
        """Convert Heurist field type to Python type.

        Args:
            datatype (str): Field type name.

        Returns:
            Any: Python type.
        """

        if datatype == cls.dropdown:
            return Optional[str]

        elif datatype == cls.numeric:
            return Optional[float]

        elif datatype == cls.single_line:
            return Optional[str]

        elif datatype == cls.multi_line:
            return Optional[str]

        elif datatype == cls.date_time:
            return dict

        elif datatype == cls.geospatial:
            return Optional[str]

        elif datatype == cls.file_or_media_url:
            return Optional[str]

        elif datatype == cls.record_pointer:
            return Optional[int]

        elif datatype == cls.relationship_marker:
            return Optional[str]

        else:
            return Optional[str]
