from pydantic import BaseModel, Field, create_model

from src.heurist_transformers.dynamic_pydantic_data_field import DynamicDataFieldBuilder
from src.sql_models.sql_safety import SafeSQLName


class DynamicRecordTypeModel:
    def __init__(self, rty_ID: int, rty_Name: str, detail_metadata: list[dict]) -> None:
        """_summary_
        The detail metadata includes the following keys: dty_ID, rst_DisplayName, \
            dty_Type, rst_MaxValues.

        Args:
            rty_ID (int): The Heurist ID of the targeted record type.
            rty_Name (str): The name of the targeted record type.
            detail_metadata (list[dict]): A list of information about the targeted \
                record's details.
        """

        self.rty_ID = rty_ID
        self.rty_Name = rty_Name
        self.table_name = SafeSQLName().create_table_name(record_name=rty_Name)
        self.model = self.to_pydantic_model(detail_metadata)

    def to_pydantic_model(self, detail_metadata: list[dict]) -> BaseModel:
        """Take a list of key-value pairs (dict), which pair a record's detail \
            (data field) with a value,
            and convert that set of key-value pairs to a Pydantic model.

        Args:
            detail_metadata (list[dict]): A record type's details, including the \
                following keys:
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
                    default=0,
                    alias="rec_ID",
                    validation_alias="rec_ID",
                    serialization_alias="H-ID",
                ),
            ),
            "type": (
                int,
                Field(
                    default=0,
                    alias="rec_RecTypeID",
                    validation_alias="rec_RecTypeID",
                    serialization_alias="type_id",
                ),
            ),
        }

        # Convert each of the record's details into a Pydantic kwarg
        for detail in detail_metadata:
            # Add the field's default parsed value
            builder = DynamicDataFieldBuilder(**detail)
            field = builder.simple_field()
            kwargs.update(field)

            if detail["dty_Type"] == "date":
                field = builder.temporal_object()
                kwargs.update(field)

            elif detail["dty_Type"] == "enum":
                field = builder.term_id()
                kwargs.update(field)

        # Using Pydantic's 'create_model' module, build the dynamic model
        return create_model(self.table_name, **kwargs)
