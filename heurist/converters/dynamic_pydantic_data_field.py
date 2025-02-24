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
        return RecordDetailConverter._fieldname(self.dty_ID)

    @property
    def _base_sql_safe_alias(self) -> str:
        return SafeSQLName().create_column_name(
            field_name=self.rst_DisplayName, field_type=self.dty_Type
        )

    @property
    def _base_pydantic_data_type(self) -> Any:
        return HeuristDataType.to_pydantic(datatype=self.dty_Type)

    def is_type_repeatable(self) -> bool:
        if self.rst_MaxValues == 0:
            return True
        else:
            return False

    def _compose_annotation(self) -> dict:
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
        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias
        self.serialization_alias = self._base_sql_safe_alias

        if self.is_type_repeatable():
            self.pydantic_type = list[self._base_pydantic_data_type]
        else:
            self.pydantic_type = self._base_pydantic_data_type

        return self._compose_annotation()

    def temporal_object(self) -> dict:
        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias + "_TEMPORAL"
        self.serialization_alias = self._base_sql_safe_alias + "_TEMPORAL"

        if self.is_type_repeatable():
            self.pydantic_type = list[Optional[dict]]
        else:
            self.pydantic_type = Optional[dict]

        return self._compose_annotation()

    def term_id(self) -> dict:
        self.reset_mutable_attributes()

        self.validation_alias = self._base_pydantic_alias + "_TRM"
        self.serialization_alias = self._base_sql_safe_alias + " TRM-ID"

        if self.is_type_repeatable():
            self.pydantic_type = list[Optional[int]]
        else:
            self.pydantic_type = Optional[int]

        return self._compose_annotation()
