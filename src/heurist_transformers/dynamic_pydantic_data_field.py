from typing import Any, Optional

from pydantic import Field

from src.heurist_transformers.detail_converter import (
    HeuristDataType,
    RecordDetailConverter,
)
from src.sql_models.sql_safety import SafeSQLName


class DynamicDataFieldBuilder:
    def __init__(
        self, dty_ID: int, rst_DisplayName: str, dty_Type: str, rst_MaxValues: int
    ):
        self.dty_ID = dty_ID
        self.rst_DisplayName = rst_DisplayName
        self.dty_Type = dty_Type
        self.rst_MaxValues = rst_MaxValues

    @property
    def base_pydantic_alias(self) -> str:
        return RecordDetailConverter._fieldname(self.dty_ID)

    @property
    def base_sql_safe_alias(self) -> str:
        return SafeSQLName().create_column_name(
            field_name=self.rst_DisplayName, field_type=self.dty_Type
        )

    @property
    def base_pydantic_data_type(self) -> Any:
        return HeuristDataType.to_pydantic(self.dty_Type)

    def is_type_repeatable(self) -> bool:
        if self.rst_MaxValues == 0:
            return True
        else:
            return False

    def _compose_annotation(
        self, validation_alias: str, pydantic_type: Any, serialization_alias: str
    ) -> dict:
        return {
            validation_alias: (
                pydantic_type,
                Field(
                    # ID of the column's data type in Heurist
                    description=self.dty_ID,
                    # Formatted way to identify the Pydantic column
                    validation_alias=validation_alias,
                    # SQL-safe version of the column name
                    serialization_alias=serialization_alias,
                    default=None,
                ),
            )
        }

    def simple_field(self) -> dict:
        if self.is_type_repeatable():
            pydantic_type = list[self.base_pydantic_data_type]
        else:
            pydantic_type = self.base_pydantic_data_type

        validation_alias = self.base_pydantic_alias
        serialization_alias = self.base_sql_safe_alias

        return self._compose_annotation(
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            pydantic_type=pydantic_type,
        )

    def temporal_object(self) -> dict:
        validation_alias = self.base_pydantic_alias + "_TEMPORAL"
        serialization_alias = self.base_sql_safe_alias + "_TEMPORAL"
        if self.is_type_repeatable():
            pydantic_type = list[Optional[dict]]
        else:
            pydantic_type = Optional[dict]

        return self._compose_annotation(
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            pydantic_type=pydantic_type,
        )

    def term_id(self) -> dict:
        if self.is_type_repeatable():
            pydantic_type = list[Optional[int]]
        else:
            pydantic_type = Optional[int]
        validation_alias = self.base_pydantic_alias + "_TRM"
        serialization_alias = self.base_sql_safe_alias + " TRM-ID"

        return self._compose_annotation(
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            pydantic_type=pydantic_type,
        )
