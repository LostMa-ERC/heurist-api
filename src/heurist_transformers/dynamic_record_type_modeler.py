from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, create_model

from src.heurist_transformers.detail_converter import (
    HeuristDataType,
    RecordDetailConverter,
)
from src.sql_models.sql_safety import SafeSQLName


class RecordTypeModeler:
    def __init__(self, rty_ID: int, rty_Name: str, detail_metadata: list[dict]) -> None:
        """_summary_
        The detail metadata includes the following keys: dty_ID, rst_DisplayName, dty_Type, rst_MaxValues.

        Args:
            rty_ID (int): The Heurist ID of the targeted record type.
            rty_Name (str): The name of the targeted record type.
            detail_metadata (list[dict]): A list of information about the targeted record's details.
        """

        self.rty_ID = rty_ID
        self.rty_Name = rty_Name
        self.table_name = SafeSQLName().create_table_name(record_name=rty_Name)
        self.model = self.to_pydantic_model(detail_metadata)

    def to_pydantic_model(self, detail_metadata: list[dict]) -> BaseModel:
        """Take a list of key-value pairs (dict), which pair a record's detail (data field) with a value,
            and convert that set of key-value pairs to a Pydantic model.

        Examples:
            >>> # Example set of key-value pairs for a record that has only one data field, i.e. 'Name or Title'.
            >>> detail_metadata = [{'dty_ID': 1, 'rst_DisplayName': 'Name or Title', 'dty_Type': 'freetext', 'rst_MaxValues': 1}]
            >>>
            >>> # Model the data for the record's details (data fields), in this case one data field.
            >>> rectype = RecordTypeModeler(rty_ID=101, rty_Name="test record", detail_metadata=detail_metadata)
            >>>
            >>> # Confirm the record was succesfully modeled and has the correct name.
            >>> rectype.model.__name__
            'TestRecord'

        Args:
            detail_metadata (list[dict]): A record type's details, including the following keys:
                dty_ID,
                rst_DisplayName,
                dty_Type,
                rst_MaxValues

        Returns:
            BaseModel: Dynamically created Pydantic BaseModel for the record type
        """

        # Indifferent to the record's data fields, set up universal data fields
        # present in every dynamic Pydantic model for records of any type
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

        # Convert each of the record's details into a Pydantic kwarg
        for detail in detail_metadata:
            new_field = self.parse_detail(metadata=detail)
            kwargs.update(new_field)

        # Using Pydantic's 'create_model' module, build the dynamic model
        return create_model(self.table_name, **kwargs)

    def parse_detail(self, metadata: dict) -> dict:
        """_summary_

        Args:
            detail (dict): _description_

        Returns:
            dict: _description_
        """

        # Because we want to create 2 fields in the case of dates, one with
        # parsed datetime objects, the other with the raw JSON date object,
        # create an empty dictionary.
        new_fields = {}

        # Parse the data field's type and format its name
        base_dtype = HeuristDataType.to_pydantic(metadata["dty_Type"])
        name = RecordDetailConverter._fieldname(metadata["dty_ID"])
        if (
            not base_dtype == list[Optional[datetime]]
            and metadata["rst_MaxValues"] == 0
        ):
            dtype = list[base_dtype]
        else:
            dtype = base_dtype

        new_fields.update(
            {
                name: (
                    dtype,
                    Field(
                        alias=metadata["rst_DisplayName"],
                        validation_alias=name,
                        serialization_alias=SafeSQLName().create_column_name(
                            field_name=metadata["rst_DisplayName"],
                            field_type=metadata["dty_Type"],
                        ),
                        default=None,
                        required=False,
                    ),
                )
            }
        )

        # If the data field is a date, create an additional field for its original JSON object form
        if dtype == list[Optional[datetime]]:
            name = RecordDetailConverter._fieldname(metadata["dty_ID"], temp=True)
            sql_safe_name = (
                SafeSQLName().create_column_name(
                    field_name=metadata["rst_DisplayName"],
                    field_type=metadata["dty_Type"],
                )
                + "_temporal"
            )
            new_fields.update(
                {
                    name: (
                        Optional[dict],
                        Field(
                            alias=f"{metadata["rst_DisplayName"]}_TEMPORAL",
                            validation_alias=name,
                            serialization_alias=sql_safe_name,
                            default=None,
                            required=False,
                        ),
                    )
                }
            )

        return new_fields
