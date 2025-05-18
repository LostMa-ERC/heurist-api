"""Class for converting a record's detail before the Pydantic model validation."""

from heurist.models.dynamic.date import TemporalObject
from heurist.models.dynamic.type import FieldType


class DetailValidator:
    """
    In Heurist, a record's "detail" is what is more commonly known as an attribute, \
        dimension, or a data field.

    This class features methods to extract the key value from Heurist's JSON \
        formatting for all data types in Heurist's system.
    """

    direct_values = ["freetext", "blocktext", "integer", "boolean", "float"]

    @classmethod
    def validate_file(cls, detail: dict) -> str:
        """
        Extract the value of a file field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail.get("value", {}).get("file", {}).get("ulf_ExternalFileReference")

    @classmethod
    def validate_enum(cls, detail: dict) -> str:
        """
        Extract the value of an enum field.

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        return detail["termLabel"]

    @classmethod
    def validate_geo(cls, detail: dict) -> str:
        """
        Extract the value of a geo field.

        Examples:
            >>> from mock_data.geo.single import DETAIL_POINT
            >>> DetailValidator.convert(DETAIL_POINT)
            'POINT(2.19726563 48.57478991)'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        geo = detail["value"]["geo"]
        if geo["type"] == "p" or geo["type"] == "pl":
            return geo["wkt"]

    @classmethod
    def validate_date(cls, detail: dict) -> dict:
        """
        Build the variable date value into a structured dictionary.

        Examples:
            >>> # Test temporal object
            >>> from mock_data.date.compound_single import DETAIL
            >>> value = DetailValidator.convert(DETAIL)
            >>> value['start']['earliest']
            datetime.datetime(1180, 1, 1, 0, 0)

            >>> # Test direct date value
            >>> from mock_data.date.simple_single import DETAIL
            >>> value = DetailValidator.convert(DETAIL)
            >>> value['value']
            datetime.datetime(2024, 3, 19, 0, 0)

        Args:
            detail (dict): Record's detail.

        Returns:
            dict: Structured metadata for a Heurist date object.
        """

        if isinstance(detail.get("value"), dict):
            model = TemporalObject.model_validate(detail["value"])
        else:
            model = TemporalObject.model_validate(detail)
        return model.model_dump(by_alias=True)

    @classmethod
    def validate_resource(cls, detail: dict) -> int:
        """
        Extract the value of a resource (foreign key) field.

        Args:
            detail (dict): Record's detail.

        Returns:
            int: Heurist ID of the referenced record.
        """

        return int(detail["value"]["id"])

    @classmethod
    def convert(cls, detail: dict) -> str | int | list | dict | None:
        """
        Based on the data type, convert the record's nested detail to a flat value.

        Args:
            detail (dict): One of the record's details (data fields).

        Returns:
            str | int | list | dict | None: Flattened value of the data field.
        """

        fieldtype = FieldType.from_detail(detail)

        if any(ft in fieldtype for ft in cls.direct_values):
            return detail["value"]

        elif fieldtype == "date":
            return cls.validate_date(detail)

        elif fieldtype == "enum":
            return cls.validate_enum(detail)

        elif fieldtype == "file":
            return cls.validate_file(detail)

        elif fieldtype == "geo":
            return cls.validate_geo(detail)

        elif fieldtype == "resource":
            return cls.validate_resource(detail)
