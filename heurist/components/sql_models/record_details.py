from pydantic import BaseModel, Field, create_model
from heurist.components.heurist.convert_record_detail import (
    HeuristDataType,
    HeuristRecordDetail,
)
import re


def clean_name(name: str) -> str:
    s = name
    # Remove parentheses
    s = re.sub(r"\(.+\)", "", s)
    # Remove non-letters
    s = re.sub(r"\W", "_", s)
    # Remove backslashes
    s = re.sub(r"/", "_", s)
    # Remove spaces
    s = re.sub(r"\s", "_", s)
    # Remove double underscores
    s = re.sub(r"_+", "_", s)
    # Trim underscores
    s = s.strip("_")
    return s


def clean_detail(detail: dict):
    name, id, dtype = detail["dty_Name"], detail["dty_ID"], detail["dty_Type"]
    s = clean_name(name)
    s = s.lower() + f" DTY{id}"
    if dtype == "resource":
        s += " H-ID"
    return s


def to_camel_case(text: str) -> str:
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return "".join(i.capitalize() for i in s)


class RecordTypeModeler:
    def __init__(self, rty_ID: int, rty_Name: str, detail_dicts: list[dict]) -> None:
        self.rty_ID = rty_ID
        self.rty_Name = rty_Name
        self.table_name = to_camel_case(rty_Name)
        self.model = self.to_pydantic_model(detail_dicts)

    def to_pydantic_model(self, detail_dicts: list[dict]) -> BaseModel:
        """_summary_

        Examples:
            >>> detail_dicts = [{'dty_ID': 1, 'dty_Name': 'Name or Title', 'dty_Type': 'freetext'}]
            >>> rectype = RecordTypeModeler(rty_ID=101, rty_Name="test record", detail_dicts=detail_dicts)
            >>> rectype.model.__name__
            'TestRecord'

        Args:
            detail_dicts (list[dict]): Details of a record type, including the following keys:
                dty_ID,
                dty_Name,
                dty_Type

        Returns:
            BaseModel: Dynamically created Pydantic BaseModel for the record type
        """

        kwargs = {
            "id": (
                int,
                Field(
                    required=True,
                    default=0,
                    alias="rec_ID",
                    validation_alias="rec_ID",
                    serialization_alias="H-ID",
                ),
            ),
            "type": (
                int,
                Field(
                    required=True,
                    default=0,
                    alias="rec_RecTypeID",
                    validation_alias="rec_RecTypeID",
                    serialization_alias="type_id",
                ),
            ),
        }
        for detail in detail_dicts:
            dtype = HeuristDataType.to_pydantic(detail["dty_Type"])
            name = HeuristRecordDetail._fieldname(detail)
            kwargs.update(
                {
                    name: (
                        dtype,
                        Field(
                            alias=detail["dty_Name"],
                            validation_alias=name,
                            serialization_alias=clean_detail(detail),
                            default=None,
                            required=False,
                        ),
                    )
                }
            )
        return create_model(self.table_name, **kwargs)
