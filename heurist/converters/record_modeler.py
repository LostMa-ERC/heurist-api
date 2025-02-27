from datetime import datetime
from typing import Union

from heurist.converters.detail_converter import RecordDetailConverter
from heurist.converters.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)
from heurist.converters.type_handler import HeuristDataType
from heurist.converters.exceptions import (
    RepeatedValueInSingularDetailType,
    DateNotEnteredAsDateObject,
)

from logging import Logger


class RecordModeler:

    def __init__(
        self,
        pydantic_model: DynamicRecordTypeModel,
        record: dict,
        logger: Logger,
        require_date_object: bool = False,
    ):
        """
        Class for validating a Heurist record's data according to the dynamically \
            created Pydantic model.

        Args:
            pydantic_model (DynamicRecordTypeModel): Pydantic model.
            record (dict): A Heurist record JSON object.
            logger (Logger): Logger for record model validation.
            require_date_object (bool): Whether to require date data types to have a \
                dictionary / JSON object, rather than a simple value. Defaults to False.
        """
        self.logger = logger
        self.plural_fields = [
            v.description
            for v in pydantic_model.model.model_fields.values()
            if repr(v.annotation).startswith("list")
            and not v.annotation == list[Union[datetime, None]]
        ]
        self.model = pydantic_model
        self.record = record
        self.details = record["details"]
        self.require_date_object = require_date_object

    def log_message(self, dty_ID: int, error_message: str) -> str:
        header = f"Record: {self.model.rty_Name}\tRecord ID: {self.record["rec_ID"]}"
        return header + f"\nDTY: {dty_ID}\t{error_message}\n"

    def log_warning(self, dty_ID: int, error_message: str) -> None:
        message = self.log_message(dty_ID=dty_ID, error_message=error_message)
        self.logger.warning(message)

    def log_error(self, dty_ID: int, error_message: str) -> None:
        message = self.log_message(dty_ID=dty_ID, error_message=error_message)
        self.logger.error(message)

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

    def valid_heurist_date_objects(self, dty_id: int, details: list[dict]) -> bool:
        for detail in details:
            # If all of the date field's values are not dictionaries, log a warning.
            if not isinstance(detail["value"], dict):
                e = DateNotEnteredAsDateObject(detail_type_id=dty_id)
                self.log_warning(dty_ID=dty_id, error_message=e.message)
                return False
        else:
            return True

    def convert_date_to_pydantic_kwarg(self, dty_id: int, details: list[dict]) -> dict:
        # Create a field annotation for the parsed date
        # (array containing the earliest and latest datetime objects).
        generic_kwarg = self.convert_generic_to_pydantic_kwarg(
            dty_id=dty_id, details=details
        )

        # Create a supplemental annotation for the date's raw JSON object.
        key = self.get_temporal_key(dty_id=dty_id)

        # If running a strict validation, check the date field's data type.
        if self.require_date_object:
            # If all the date values are valid Heurist date objects, extract them.
            if self.valid_heurist_date_objects(dty_id=dty_id, details=details):
                converted_values = [d["value"] for d in details]
            # If any of the date values were not valid Heurist date objects, stop
            # and simply return the field annotation of the generic date field.
            else:
                return generic_kwarg

        # If not checking the date field's data type, ignore non-dictionary
        # values for the supplemental temporal column.
        else:
            converted_values = [
                d["value"] for d in details if isinstance(d["value"], dict)
            ]

        # If the data field allows multiple values, return the list
        if self.is_plural(dty_id=dty_id):
            date_object_kwarg = {key: converted_values}

        # If the data field is limited to 1 value and has 1 validated value
        # return it.
        elif len(converted_values) == 1:
            date_object_kwarg = {key: converted_values[0]}
        # If using a relaxed validation of the Heurist date object value and no values
        # passed, create an empty dictionary for the supplemental column's annotation.
        elif not self.require_date_object:
            date_object_kwarg = {}

        # Combine the generic and supplemental annotations in 1 dictionary.
        return generic_kwarg | date_object_kwarg

    def flatten_record_details(self) -> dict:

        details_aggregated_by_types = self.aggregate_details(self.details)

        # Flatten the aggregated details into a set of key-value pairs, wherein
        # the key is the same fieldname used to create the dynamic Pydantic model.
        flat_details = {}
        for dty_id, details in details_aggregated_by_types.items():

            # If the detail is limited to a maximum of 1 values, log the error
            # that there are more than 1 details aggregated in this detail type.
            value_count = len(details)
            if not self.is_plural(dty_id=dty_id) and value_count > 1:
                e = RepeatedValueInSingularDetailType(
                    detail_type_id=dty_id,
                    value_count=value_count,
                )
                self.log_error(dty_ID=dty_id, error_message=e.message)
                continue

            # If the detail has a valid amount of values, continue.
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
