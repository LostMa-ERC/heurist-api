from datetime import datetime
from typing import Union

from heurist.converters.detail_converter import RecordDetailConverter
from heurist.converters.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)
from heurist.converters.type_handler import HeuristDataType


class RecordModeler:
    def __init__(self, pydantic_model: DynamicRecordTypeModel, record: dict):
        self.plural_fields = [
            v.description
            for v in pydantic_model.model.model_fields.values()
            if repr(v.annotation).startswith("list")
            and not v.annotation == list[Union[datetime, None]]
        ]
        self.record = record
        self.details = record["details"]

    def is_plural(self, dty_id: int) -> bool:
        return dty_id in self.plural_fields

    @staticmethod
    def aggregate_details(details: list[dict]) -> dict:
        unique_detail_type_ids = set([d["dty_ID"] for d in details])
        details_aggregated_by_type = {i: [] for i in unique_detail_type_ids}
        for detail in details:
            detail_type_id = detail["dty_ID"]
            details_aggregated_by_type[detail_type_id].append(detail)
        return details_aggregated_by_type

    @staticmethod
    def get_generic_key(dty_id: int) -> str:
        return RecordDetailConverter._fieldname(dty_id)

    @classmethod
    def get_temporal_key(cls, dty_id: int) -> str:
        return cls.get_generic_key(dty_id=dty_id) + "_TEMPORAL"

    @classmethod
    def get_term_key(cls, dty_id: int) -> str:
        return cls.get_generic_key(dty_id=dty_id) + "_TRM"

    def convert_generic_to_pydantic_kwarg(
        self, dty_id: int, details: list[dict]
    ) -> dict:
        key = self.get_generic_key(dty_id=dty_id)
        converted_values = [RecordDetailConverter._convert_value(d) for d in details]
        if self.is_plural(dty_id=dty_id):
            return {key: converted_values}
        else:
            return {key: converted_values[0]}

    def convert_enum_to_pydantic_kwarg(self, dty_id: int, details: list[dict]) -> dict:
        generic_kwarg = self.convert_generic_to_pydantic_kwarg(
            dty_id=dty_id, details=details
        )
        key = self.get_term_key(dty_id=dty_id)
        converted_values = [int(d["value"]) for d in details]
        if self.is_plural(dty_id=dty_id):
            enum_kwarg = {key: converted_values}
        else:
            enum_kwarg = {key: converted_values[0]}
        return generic_kwarg | enum_kwarg

    def convert_date_to_pydantic_kwarg(self, dty_id: int, details: list[dict]) -> dict:
        generic_kwarg = self.convert_generic_to_pydantic_kwarg(
            dty_id=dty_id, details=details
        )
        key = self.get_temporal_key(dty_id=dty_id)
        converted_values = [d["value"] for d in details]
        if self.is_plural(dty_id=dty_id):
            enum_kwarg = {key: converted_values}
        else:
            enum_kwarg = {key: converted_values[0]}
        return generic_kwarg | enum_kwarg

    def flatten_record_details(self) -> dict:

        details_aggregated_by_types = self.aggregate_details(self.details)

        # Flatten the aggregated details into a set of key-value pairs, wherein
        # the key is the same fieldname used to create the dynamic Pydantic model.
        flat_details = {}
        for dty_id, details in details_aggregated_by_types.items():

            fieldtype = HeuristDataType.from_json_record(details[0])

            if fieldtype == "enum":
                kwarg = self.convert_enum_to_pydantic_kwarg(
                    dty_id=dty_id,
                    details=details,
                )
                flat_details.update(kwarg)

            elif fieldtype == "date":
                kwarg = self.convert_date_to_pydantic_kwarg(
                    dty_id=dty_id,
                    details=details,
                )
                flat_details.update(kwarg)

            else:
                kwarg = self.convert_generic_to_pydantic_kwarg(
                    dty_id=dty_id,
                    details=details,
                )
                flat_details.update(kwarg)

        # Add in universal fields for the dynamic Pydantic model
        flat_details.update(
            {
                "rec_ID": self.record["rec_ID"],
                "rec_RecTypeID": self.record["rec_RecTypeID"],
            }
        )

        return flat_details
