from typing import Any, Optional

from pydantic import Field

from heurist.converters.detail_converter import (
    HeuristDataType,
    RecordDetailConverter,
)
from heurist.sql.sql_safety import SafeSQLName


class DynamicDataFieldBuilder:
    def __init__(
        self, dty_ID: int, rst_DisplayName: str, dty_Type: str, rst_MaxValues: int
    ):
        """
        Using information of 1 detail (data field) from a Heurist record, build a \
            Pydantic data field annotation.

        Args:
            dty_ID (int): Detail's ID.
            rst_DisplayName (str): Name of the detail displayed in Heurist.
            dty_Type (str): Detail's data type.
            rst_MaxValues (int): Heurist indicator if the detail can be repeated.
        """

        self.dty_ID = dty_ID
        self.rst_DisplayName = rst_DisplayName
        self.dty_Type = dty_Type
        self.rst_MaxValues = rst_MaxValues
        # Mutable, reset on class instance
        self.pydantic_type = None
        self.validation_alias = None
        self.serialization_alias = None

    def reset_mutable_attributes(self):
        self.pydantic_type = None
        self.validation_alias = None
        self.serialization_alias = None

    @property
    def _base_pydantic_alias(self) -> str:
        """
        Apply the `RecordDetailConverter`'s `_fieldname` method to the detail's ID \
            to generate a consistent alias for the Pydantic model.
        """

        return RecordDetailConverter._fieldname(self.dty_ID)

    @property
    def _base_sql_safe_alias(self) -> str:
        """
        Apply the `SafeSQLName`'s `create_column_name` method to the detail's ID and \
            the record structure's display name to generate an SQL-safe column name.
        """

        return SafeSQLName().create_column_name(
            field_name=self.rst_DisplayName, field_type=self.dty_Type
        )

    @property
    def _base_pydantic_data_type(self) -> Any:
        """
        Apply the `HeuristDataType`'s `to_pydantic` method to the detail's data \
            type to get the corresponding Python data type.
        """

        return HeuristDataType.to_pydantic(datatype=self.dty_Type)

    def is_type_repeatable(self) -> bool:
        """
        Heurist uses the code 0 to indicate that the a record's detail (field) \
            can be repeated. Parse this information on the record structure \
            to determine a boolean indicating whether or not the detail is repeated.

        Returns:
            bool: Whether the detail can be repeated.
        """

        if self.rst_MaxValues == 0:
            return True
        else:
            return False

    def _compose_annotation(self) -> dict:
        """
        Using the Heurist information stored in the class instance's attributes, build \
            the Pydantic data field's alias and compose its annotation.

        Returns:
            dict: Key-value pair: Pydantic field's alias (key) - annotation (value)
        """

        if not self.validation_alias:
            raise ValueError()
        if not self.serialization_alias:
            raise ValueError()
        if not self.pydantic_type:
            raise ValueError()

        if self.rst_MaxValues == 0:
            default = []
        else:
            default = None

        return {
            self.validation_alias: (
                self.pydantic_type,
                Field(
                    # ID of the column's data type in Heurist
                    description=self.dty_ID,
                    # Formatted way to identify the Pydantic column
                    validation_alias=self.validation_alias,
                    # SQL-safe version of the column name
                    serialization_alias=self.serialization_alias,
                    # Default value to write in DuckDB column
                    default=default,
                ),
            )
        }

    def simple_field(self) -> dict:
        """
        Build a Pydantic field annotation for a detail whose value will simply be the \
            result of the `RecordDetailConverter`, meaning not a date and not a \
            vocabulary term.

        Returns:
            dict: Pydantic field annotation.
        """

        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias
        self.serialization_alias = self._base_sql_safe_alias

        if self.is_type_repeatable():
            self.pydantic_type = list[self._base_pydantic_data_type]
        else:
            self.pydantic_type = self._base_pydantic_data_type

        return self._compose_annotation()

    def temporal_object(self) -> dict:
        """
        Build a Pydantic field annotation for the raw JSON of Heurist's date object. \
        This field is written to the Pydantic model in addition to a simpler column \
        for the date field with the earliest and latest dates parsed as datetime \
        objects.

        Returns:
            dict: Pydantic field annotation.
        """

        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias + "_TEMPORAL"
        self.serialization_alias = self._base_sql_safe_alias + "_TEMPORAL"

        if self.is_type_repeatable():
            self.pydantic_type = list[Optional[dict]]
        else:
            self.pydantic_type = Optional[dict]

        return self._compose_annotation()

    def term_id(self) -> dict:
        """
        Build a Pydantic field annotation for a foreign key refernce to the vocabulary \
            term in the constructed database's trm table. This field is written to the \
            Pydantic model in addition to a column for the term that simply has the \
            label.

        Returns:
            dict: Pydantic field annotation.
        """

        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias + "_TRM"
        self.serialization_alias = self._base_sql_safe_alias + " TRM-ID"

        if self.is_type_repeatable():
            self.pydantic_type = list[Optional[int]]
        else:
            self.pydantic_type = Optional[int]

        return self._compose_annotation()
