from datetime import datetime
from typing import Any, Union

from pydantic import BaseModel

from heurist.converters.detail_converter import RecordDetailConverter
from heurist.converters.type_handler import HeuristDataType


class RecordFlattener:
    """Prepare array of record details for Pydantic model validation."""

    def __init__(self, pydantic_model: BaseModel):
        self.model = pydantic_model

    @staticmethod
    def aggregate_details(record_details: list[dict]) -> dict:
        aggregated_details = {}
        for detail in record_details:
            detail_type_id = detail["dty_ID"]
            if not aggregated_details.get(detail_type_id):
                aggregated_details.update({detail_type_id: []})
            aggregated_details[detail_type_id].append(detail)
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
            detail["value"]
            for detail in details
            if isinstance(detail.get("value"), dict)
        ]
        if len(objects) > 0:
            if plural:
                return objects
            else:
                return objects[0]

    def make_enum_field(self, details: list[dict], plural: bool) -> int | list | None:
        term_ids = [detail.get("value") for detail in details]
        if plural:
            return [int(i) for i in term_ids]
        else:
            return int(term_ids[0])

    def __call__(self, record_details: list[dict]) -> dict:
        if not isinstance(record_details, list):
            raise TypeError("Details must be a list.")

        # Aggregate details by ID
        aggregated_details = self.aggregate_details(record_details)

        # Set up empty dictionary to hold unique / unified Pydantic fields
        kwargs = {}

        # Update the Pydantic keys dictionary with values
        for dty_ID, details in aggregated_details.items():
            first_detail = details[0]
            # Parse the detail type's data type
            fieldtype = HeuristDataType.from_json_record(first_detail)

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

            if fieldtype == "enum":
                key = RecordDetailConverter._fieldname(dty_ID=dty_ID) + "_TRM"
                value = self.make_enum_field(details=details, plural=plural)
                kwargs.update({key: value})

        return kwargs
