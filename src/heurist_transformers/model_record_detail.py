"""Class for converting a record's detail before the Pydantic model validation."""

from typing import Generator

from src.heurist_transformers.type_handler import HeuristDataType
from src.heurist_transformers.date_handler import HeuristDateHandler


class HeuristRecordDetail:
    direct_values = ["freetext", "blocktext", "integer", "boolean", "float"]

    def __init__(self) -> None:
        pass

    def __call__(self, details: list[dict]) -> Generator[dict | None, None, None]:
        """_summary_

        Args:
            details (list[dict]): _description_

        Returns:
            _type_: s_description_

        Yields:
            Generator[dict|None, None, None]: _description_
        """

        for detail in details:
            fieldtype = HeuristDataType.from_json_record(detail)
            flattened_detail = self.convert_to_dict(detail)

            # Skip this detail if it has no value
            if not flattened_detail:
                continue

            results = [flattened_detail]

            # If the detail is a date, give the parsed datetime objects and the original JSON
            if fieldtype == "date":
                value = detail["value"]
                if type(value) == dict:
                    key = self._fieldname(detail, temp=True)
                    value = detail["value"]
                    supplemental_detail = {key: value}
                    results.append(supplemental_detail)

            yield from results

    @classmethod
    def convert_to_dict(cls, detail: dict) -> dict | None:
        """Convert the record's detail to a key-value pair.

        Args:
            detail (dict): Record's detail.

        Returns:
            dict: Key-value pair of the field's name and flattened value.
        """

        key = cls._fieldname(detail)
        value = cls._convert_value(detail)
        if value:
            return {key: value}

    @classmethod
    def file(cls, detail: dict) -> str:
        """Extract the value of a file field.

        Examples:
            >>> detail = {
            ...     "dty_ID": 1113,
            ...     "value": {
            ...         "file": {
            ...             "ulf_ID": "1",
            ...             "fullPath": None,
            ...             "ulf_ExternalFileReference": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg",
            ...             "fxm_MimeType": "image/jpeg",
            ...             "ulf_PreferredSource": "local",
            ...             "ulf_OrigFileName": "_remote",
            ...             "ulf_FileSizeKB": "0",
            ...             "ulf_ObfuscatedFileID": "286ccc9935b4ac7d2ba372b561c5ce9a5ae609dd",
            ...             "ulf_Description": "",
            ...             "ulf_Added": "2024-04-05 21:48:05",
            ...             "ulf_MimeExt": "jpe",
            ...             "ulf_Caption": "seagull from wikimedia images",
            ...             "ulf_Copyright": "",
            ...             "ulf_Copyowner": ""
            ...         },
            ...         "fileid": "286ccc9935b4ac7d2ba372b561c5ce9a5ae609dd"
            ...     },
            ...     "fieldName": "file or media url",
            ...     "fieldType": "file",
            ...     "conceptID": ""
            ... }
            >>> HeuristRecordDetail.file(detail)
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
            >>> detail = {
            ...     "dty_ID": 1107,
            ...     "value": "5391",
            ...     "termLabel": "Disease",
            ...     "termConceptID": "2-5391",
            ...     "fieldName": "dropdown",
            ...     "fieldType": "enum",
            ...     "conceptID": "",
            ... }
            >>> HeuristRecordDetail.enum(detail)
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
            >>> detail = {
            ...     "dty_ID": 1112,
            ...     "value": {
            ...         "geo": {
            ...             "type": "p",
            ...             "wkt": "POINT(2.19726563 48.57478991)"
            ...         }
            ...     },
            ...     "fieldName": "geospatial",
            ...     "fieldType": "geo",
            ...     "conceptID": ""
            ... }
            >>> HeuristRecordDetail.geo(detail)
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
            >>> detail = {
            ...     "dty_ID": 9,
            ...     "value": {
            ...         "comment": "Some comments here about the fuzzy date.",
            ...         "start": {
            ...             "earliest": "1248",
            ...             "latest": "1248-05-01"
            ...         },
            ...         "end": {
            ...             "earliest": "1312-08-29",
            ...             "latest": "1350"
            ...         },
            ...         "estMinDate": 1248,
            ...         "estMaxDate": 1350.1231
            ...     },
            ...     "fieldName": "Date",
            ...     "fieldType": "date",
            ...     "conceptID": "2-9"
            ... }
            >>> HeuristRecordDetail.date(detail)
            [datetime.datetime(1248, 1, 1, 0, 0), datetime.datetime(1350, 12, 31, 0, 0)]
            >>>
            >>> detail = {
            ...     "dty_ID": 1111,
            ...     "value": 2024,
            ...     "fieldName": "date / time",
            ...     "fieldType": "date",
            ...     "conceptID": ""
            ... }
            >>> HeuristRecordDetail.date(detail)
            [datetime.datetime(2024, 1, 1, 0, 0), None]

        Args:
            detail (dict): Record's detail.

        Returns:
            list: List of one or two dates.
        """

        value = detail["value"]
        handler = HeuristDateHandler()
        if (
            isinstance(value, dict)
            and "end" in value.keys()
            and "start" in value.keys()
        ):
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
            >>> detail = {
            ...     "dty_ID": 1097,
            ...     "value": {
            ...         "id": "126",
            ...         "type": "103",
            ...         "title": "Chevalerie Ogier",
            ...         "hhash": None
            ...     },
            ...     "fieldName": "work",
            ...     "fieldType": "resource",
            ...     "conceptID": ""
            ... }
            >>> HeuristRecordDetail.resource(detail)
            '126'

        Args:
            detail (dict): Record's detail.

        Returns:
            str: Value of record's detail.
        """

        value = detail["value"]
        return value["id"]

    @classmethod
    def _fieldname(cls, detail: dict, temp: bool = False) -> str:
        supp = ""
        if temp:
            supp = "_TEMPORAL"
        return f"DTY{detail['dty_ID']}{supp}"

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
