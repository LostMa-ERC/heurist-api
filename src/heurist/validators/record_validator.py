import logging
import os
from pathlib import Path

from heurist.models.dynamic.annotation import PydanticField
from heurist.models.dynamic.type import FieldType
from heurist.validators.detail_validator import DetailValidator
from heurist.validators.exceptions import RepeatedValueInSingularDetailType
from pydantic import BaseModel

VALIDATION_LOG = Path.cwd().joinpath("validation.log")

handlers = [logging.FileHandler(filename=VALIDATION_LOG, mode="w", delay=True)]
if os.getenv("HEURIST_STREAM_LOG") == "True":
    handlers.append(logging.StreamHandler())

logging.basicConfig(
    encoding="utf-8",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    handlers=handlers,
)


def list_plural_fields(pydantic_model: BaseModel) -> list:
    return [
        v.description
        for v in pydantic_model.model_fields.values()
        if repr(v.annotation).startswith("list")
    ]


class RecordValidator:
    def __init__(
        self, pydantic_model: BaseModel, records: list[dict], rty_ID: int
    ) -> None:
        self.pydantic_model = pydantic_model
        self._rty_ID = rty_ID
        self._records = records
        self._index = 0
        self._plural_fields = list_plural_fields(pydantic_model=self.pydantic_model)

    def is_plural(self, dty_ID: int) -> bool:
        if dty_ID in self._plural_fields:
            return True

    def __iter__(self):
        return self

    def __next__(self) -> BaseModel:
        if self._index < len(self._records):
            record = self._records[self._index]
            self._index += 1
            # If the record isn't of the record type for this model, skip it.
            if record["rec_RecTypeID"] != self._rty_ID:
                pass
            # Otherwise, process the record's details into key-value pairs that
            # will be loaded into the Pydantic model.
            kwargs = self.flatten_details_to_dynamic_pydantic_fields(record)
            # Return a validated Pydantic model.
            return self.pydantic_model.model_validate(kwargs)
        else:
            raise StopIteration

    @classmethod
    def aggregate_details_by_type(cls, details: list[dict]) -> dict:
        # Set up an index for all the types of details in this record's
        # sequence of details.
        index = {d["dty_ID"]: [] for d in details}
        # According to its type, add each detail to its respective list in the index.
        [index[d["dty_ID"]].append(d) for d in details]
        # Return the index of aggregated details.
        return index

    def flatten_details_to_dynamic_pydantic_fields(self, record: dict) -> dict:
        detail_type_index = self.aggregate_details_by_type(record["details"])
        # To the list of key-value pairs, add the record's H-ID and its type ID
        record_id = record["rec_ID"]
        kwargs = {
            "rec_ID": record_id,
            "rec_RecTypeID": record["rec_RecTypeID"],
        }
        for dty_ID, details in detail_type_index.items():
            # Determine if this detail type is allowed to have multiple values.
            repeats = self.is_plural(dty_ID=dty_ID)

            # If this detail is not supposed to be repeateable but Heurist allowed more
            # than 1 value to be saved in the field, raise an error.
            if not repeats and len(details) > 1:
                warning = RepeatedValueInSingularDetailType(
                    type_id=record["rec_RecTypeID"],
                    record_id=record_id,
                    field_name=details[0]["fieldName"],
                    value_count=len(details),
                )
                logging.warning(warning)
                continue

            # Get the validation alias for this kwarg's key
            key = PydanticField._get_validation_alias(dty_ID=dty_ID)

            # Convert the detail's metadata to a flat value.
            values = []
            for detail in details:
                v = DetailValidator.convert(detail=detail)
                values.append(v)

            # Check the number of validated metadata against what is permissible for
            # this detail type according to the Heurist schema.
            value = self.validate_for_repeatable_values(repeats=repeats, values=values)

            # If the validation failed, do not add this detail type to the set of
            # kwargs for the Pydantic model. Let the model's default value be used
            # for this missing / invalid metadata.
            if not value:
                continue

            # Add this detail type's alias and validated value(s) to the set of kwargs.
            kwargs.update({key: value})

            # If the detail is a Term, add an additional field for the foreign key.
            if FieldType.from_detail(details[0]) == "enum":
                # To this detail type's validation alias, which is associated with the
                # term's label, append a suffix to distinguish it as a supplemental
                # field to hold the foreign key.
                key += PydanticField.trm_validation_alias_suffix
                # Into a list, extract each detail's foreign key, which is in "value."
                values = []
                for detail in details:
                    values.append(detail["value"])

                value = self.validate_for_repeatable_values(
                    repeats=repeats, values=values
                )

                # The previous if-condition should have already confirmed that this
                # group of deatils are valid. Therefore, they can be added directly
                # to the kwargs.
                kwargs.update({key: value})

        # Return the flat key-value pairs for the Pydantic model's fields.
        return kwargs

    @classmethod
    def validate_for_repeatable_values(
        cls, repeats: bool, values: list
    ) -> list | dict | None:
        # If the detail type is not repeatable, extract the first dictionary.
        if not repeats and len(values) > 0:
            return values[0]
        # If the detail type is repeatable, send the list of values, which can
        # be an empty list--as this should be the default value for this field
        # annotation.
        elif repeats:
            return values
