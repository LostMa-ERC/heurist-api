from pydantic import BaseModel
from typing import Union, Any
from src.heurist_transformers.detail_converter import RecordDetailConverter
from src.heurist_transformers.type_handler import HeuristDataType
from datetime import datetime


class RecordFlattener:
    """Prepare array of record details for Pydantic model validation."""

    def __init__(self, pydantic_model: BaseModel):
        self.model = pydantic_model

    @staticmethod
    def aggregate_details(record_details: list[dict]) -> dict:
        aggregated_details = {}
        for d in record_details:
            if not aggregated_details.get(d["dty_ID"]):
                aggregated_details.update({d["dty_ID"]: []})
            aggregated_details[d["dty_ID"]].append(d)
        return aggregated_details

    @property
    def plural_fields(self) -> list:
        return [
            v.description
            for v in self.model.model_fields.values()
            if repr(v.annotation).startswith("list")
            and not v.annotation == list[Union[datetime, None]]
        ]

    def flatten_simple_field(self, details: list[dict], plural: bool) -> Any | None:
        if len(details) == 1:
            value = RecordDetailConverter._convert_value(details[0])
            if plural:
                value = [value]
        else:
            value = []
            for detail in details:
                value.append(RecordDetailConverter._convert_value(detail))
        return value

    def make_temporal_field(
        self, details: list[dict], plural: bool
    ) -> dict | list | None:
        objects = [
            detail.get("value")
            for detail in details
            if isinstance(detail.get("value"), dict)
        ]
        if plural:
            return objects
        else:
            print("\n\nPLURAL:{}".format(plural))
            return objects[0]

    def __call__(self, record_details: list[dict]) -> dict:
        # Aggregate details by ID
        aggregated_details = self.aggregate_details(record_details)

        # Set up empty dictionary to hold unique / unified Pydantic fields
        kwargs = {}

        # Update the Pydantic keys dictionary with values
        for dty_ID, details in aggregated_details.items():
            # Parse the detail type's data type
            fieldtype = HeuristDataType.from_json_record(details[0])

            # Parse the validation alias and whether the field is repeatable
            key = RecordDetailConverter._fieldname(dty_ID=dty_ID)
            plural = dty_ID in self.plural_fields

            # Add the basic field data
            value = self.flatten_simple_field(details=details, plural=plural)
            kwargs.update({key: value})

            # Add temporal objects if any
            if fieldtype == "date":
                key = RecordDetailConverter._fieldname(dty_ID=dty_ID) + "_TEMPORAL"
                value = self.make_temporal_field(details=details, plural=plural)
                kwargs.update({key: value})

        return kwargs
