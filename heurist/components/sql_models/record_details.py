from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, create_model

from heurist.components.heurist.convert_record_detail import (
    HeuristDataType,
    HeuristRecordDetail,
)
from heurist.components.sql_models.sql_safety import SafeSQLName


class RecordTypeModeler:
    def __init__(self, rty_ID: int, rty_Name: str, detail_dicts: list[dict]) -> None:
        self.rty_ID = rty_ID
        self.rty_Name = rty_Name
        self.table_name = SafeSQLName().create_table_name(record_name=rty_Name)
        self.model = self.to_pydantic_model(detail_dicts)

    def parse_detail(self, kwargs: dict, detail: dict) -> None:
        """_summary_

        Args:
            kwargs (dict): _description_
            detail (dict): _description_
        """

        dtype = HeuristDataType.to_pydantic(detail["dty_Type"])
        name = HeuristRecordDetail._fieldname(detail)
        kwargs.update(
            {
                name: (
                    dtype,
                    Field(
                        alias=detail["rst_DisplayName"],
                        validation_alias=name,
                        serialization_alias=SafeSQLName().create_column_name(
                            field_name=detail["rst_DisplayName"],
                            field_type=detail["dty_Type"],
                        ),
                        default=None,
                        required=False,
                    ),
                )
            }
        )

        if dtype == list[Optional[datetime]]:
            name = HeuristRecordDetail._fieldname(detail, temp=True)
            sql_safe_name = (
                SafeSQLName().create_column_name(
                    field_name=detail["rst_DisplayName"],
                    field_type=detail["dty_Type"],
                )
                + "_temporal"
            )
            kwargs.update(
                {
                    name: (
                        Optional[dict],
                        Field(
                            alias=f"{detail["rst_DisplayName"]}_TEMPORAL",
                            validation_alias=name,
                            serialization_alias=sql_safe_name,
                            default=None,
                            required=False,
                        ),
                    )
                }
            )

    def to_pydantic_model(self, detail_dicts: list[dict]) -> BaseModel:
        """Take a list of key-value pairs (dict), which pair a record's detail (data field) with a value,
            and convert that set of key-value pairs to a Pydantic model.

        Examples:
            >>> # Example set of key-value pairs for a record that has one data field.
            >>> detail_dicts = [{'dty_ID': 1, 'rst_DisplayName': 'Name or Title', 'dty_Type': 'freetext'}]
            >>>
            >>> # Model the data for the record's details (data fields), in this case one data field.
            >>> rectype = RecordTypeModeler(rty_ID=101, rty_Name="test record", detail_dicts=detail_dicts)
            >>>
            >>> # Confirm the record was succesfully modeled and has the correct name.
            >>> rectype.model.__name__
            'TestRecord'

        Args:
            detail_dicts (list[dict]): Details of a record type, including the following keys:
                dty_ID,
                rst_DisplayName,
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
            self.parse_detail(kwargs=kwargs, detail=detail)
        return create_model(self.table_name, **kwargs)
