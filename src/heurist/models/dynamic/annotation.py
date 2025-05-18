from typing import Any, Optional

from heurist.models.dynamic.type import FieldType
from heurist.sql.sql_safety import SafeSQLName
from pydantic import Field


class PydanticField:
    trm_validation_alias_suffix = "_TRM"

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

    @classmethod
    def _get_validation_alias(cls, dty_ID: int) -> str:
        return f"DTY{dty_ID}"

    @property
    def validation_alias(self) -> str:
        return self._get_validation_alias(dty_ID=self.dty_ID)

    @property
    def serlialization_alias(self) -> str:
        return SafeSQLName().create_column_name(
            field_name=self.rst_DisplayName, field_type=self.dty_Type
        )

    @property
    def pydantic_type(self) -> Any:
        fieldtype = FieldType.to_pydantic(datatype=self.dty_Type)
        if self._is_type_repeatable():
            return list[fieldtype]
        else:
            return fieldtype

    def build_field(self) -> dict:
        """
        Build a Pydantic field annotation for a detail whose value will simply be the \
            result of the `RecordDetailConverter`, meaning not a date and not a \
            vocabulary term.

        Returns:
            dict: Pydantic field annotation.
        """

        return self._compose_annotation(
            validation_alias=self.validation_alias,
            serialization_alias=self.serlialization_alias,
            pydantic_type=self.pydantic_type,
        )

    def build_term_fk(self) -> dict:
        """
        Build a Pydantic field annotation for a foreign key reference to the vocabulary\
            term in the constructed database's trm table. This field is written to the \
            Pydantic model in addition to a column for the term that simply has the \
            label.

        Returns:
            dict: Pydantic field annotation.
        """

        validation_alias = self.validation_alias + self.trm_validation_alias_suffix
        serialization_alias = self.serlialization_alias + " TRM-ID"
        if self._is_type_repeatable():
            pydantic_type = list[Optional[int]]
        else:
            pydantic_type = Optional[int]

        return self._compose_annotation(
            validation_alias=validation_alias,
            serialization_alias=serialization_alias,
            pydantic_type=pydantic_type,
        )

    def _is_type_repeatable(self) -> bool:
        """
        Heurist uses the code 0 to indicate that a record's detail (field) \
            can be repeated. Parse this information on the record structure \
            to determine a boolean indicating whether or not the detail is repeated.

        Returns:
            bool: Whether the detail can be repeated.
        """

        if self.rst_MaxValues == 0:
            return True
        else:
            return False

    def _compose_annotation(
        self, validation_alias: str, serialization_alias: str, pydantic_type: Any
    ) -> dict:
        """
        Using the Heurist information stored in the class instance's attributes, build \
            the Pydantic data field's alias and compose its annotation.

        Returns:
            dict: Key-value pair: Pydantic field's alias (key) - annotation (value)
        """

        if not validation_alias:
            raise ValueError()
        if not serialization_alias:
            raise ValueError()
        if not pydantic_type:
            raise ValueError()

        if self.rst_MaxValues == 0:
            default = []
        else:
            default = None

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
                    # Default value to write in DuckDB column
                    default=default,
                ),
            )
        }
