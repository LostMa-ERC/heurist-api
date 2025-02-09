from datetime import datetime
from typing import Union

from src import setup_logger, DATABASE_LOG

import pandas as pd
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pydantic import BaseModel

from src.database.skeleton import DatabaseSkeleton
from src.heurist_transformers.detail_converter import RecordDetailConverter
from src.heurist_transformers.dynamic_record_type_modeler import DynamicRecordTypeModel
from src.heurist_transformers.type_handler import HeuristDataType


logger = setup_logger(name="validate-pydantic-model", filepath=DATABASE_LOG)


class LoadedDatabase(DatabaseSkeleton):
    """Class for building and populating SQL tables with data collected from \
        remote Heurist DB.

    Args:
        DatabaseSkeleton (class): Class featuring methods for parsing the \
            Heurist DB schema.
    """

    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        save_structure: bool = False,
        db: str | None = ":memory:",
        record_type_groups: list[str] = ["My record types"],
    ) -> None:
        super().__init__(hml_xml, conn, db, save_structure)

        self.pydantic_models = {
            r.rty_ID: r for r in self.yield_record_details(record_type_groups)
        }

    def model_record_data(
        self, pydantic_model: DynamicRecordTypeModel, records: list[dict]
    ) -> list[BaseModel]:
        """Model the data of each record in a list of records.

        Args:
            pydantic_model (DynamicRecordTypeModel): Pydantic model created for the \
                record.
            records (list[dict]): A JSON array of a record's details.

        Yields:
            Iterator[BaseModel]: _description_
        """

        modeled_records = []

        for record in records:
            # Skip any records in the data set that are not targeted
            if record["rec_RecTypeID"] != str(pydantic_model.rty_ID):
                continue

            # See which fields permit multiple values
            plural_fields = [
                v.validation_alias
                for v in pydantic_model.model.model_fields.values()
                if repr(v.annotation).startswith("list")
                and not v.annotation == list[Union[datetime, None]]
            ]

            # Get a unique set of all the detail types on the record.
            # Heurist delivers details itemized by the value, and therefore the array of
            # details can have repeats of a detail type. We need to aggregate the values
            # by the detail type because we want one field per detail type on our model.
            dty_ids = set([d["dty_ID"] for d in record["details"]])
            details_aggregated_by_types = {i: [] for i in dty_ids}
            for d in record["details"]:
                dty_id = d["dty_ID"]
                details_aggregated_by_types[dty_id].append(d)

            # Flatten the aggregated details into a set of key-value pairs, wherein
            # the key is the same fieldname used to create the dynamic Pydantic model.
            flat_details = {}
            for dty_id, details in details_aggregated_by_types.items():
                key = RecordDetailConverter._fieldname(dty_id)
                if len(details) == 1:
                    value = RecordDetailConverter._convert_value(details[0])
                    # If this detail allows multiple values, place the value in a list.
                    if key in plural_fields:
                        value = [value]
                # If there are more than one of this detail type, then the detail must
                # allow multiple values and they must be in a list.
                else:
                    value = []
                    for detail in details:
                        value.append(RecordDetailConverter._convert_value(detail))
                flat_details.update({key: value})

                # Now we need to look into the detail type itself and add more columns
                # for date fields.
                fieldtype = HeuristDataType.from_json_record(details[0])
                if fieldtype == "date":
                    key = RecordDetailConverter._fieldname(dty_id) + "_TEMPORAL"
                    # If the detail is a temporal object, add it to the additional date
                    # column
                    if len(details) == 1 and isinstance(details[0]["value"], dict):
                        flat_details.update({key: details[0]["value"]})
                    # If any of the details are a temporal object, add them to the
                    # additional date column
                    else:
                        value = {}
                        for i, detail in enumerate(details):
                            v = detail["value"]
                            # If the date data is a temporal object, add it to the
                            # value array
                            if isinstance(v, dict):
                                value.update({i: v})
                        # Leave the field empty if there is no temporal data
                        if not value == {}:
                            flat_details.update({key: value})

            # Add in universal fields for the dynamic Pydantic model
            flat_details.update(
                {"rec_ID": record["rec_ID"], "rec_RecTypeID": record["rec_RecTypeID"]}
            )

            # Validate the flattened details inside the record type's Pydantic model
            try:
                modeled_records.append(
                    pydantic_model.model.model_validate(flat_details)
                )
            except Exception as e:
                message = f"Record ID: {record["rec_ID"]}\t{e}"
                logger.warning(message)

        # Return a list of validated Pydantic models
        return modeled_records

    def insert_records(
        self, record_type_id: int, records: list[dict]
    ) -> DuckDBPyRelation:
        """_summary_

        Args:
            records (list[dict]): _description_

        Returns:
            DuckDBPyRelation: _description_
        """

        # Given the record type's ID, get the Pydantic model created for this type
        pydantic_model = self.pydantic_models[record_type_id]

        # Model all the records' data
        modeled_records = self.model_record_data(pydantic_model, records)
        if len(modeled_records) == 0:
            return
        else:
            modeled_dicts = [m.model_dump(by_alias=True) for m in modeled_records]

        # Transform the series of models into a dataframe
        try:
            df = pd.DataFrame(modeled_dicts)
            assert df.shape[1] > 0
        except Exception as e:
            from pprint import pprint

            pprint(modeled_dicts)
            raise e

        # Delete any existing table
        self.delete_existing_table(table_name=pydantic_model.table_name)

        # From the dataframe, build a table for the record type
        sql = f"""CREATE TABLE {pydantic_model.table_name} AS FROM df"""
        self.conn.sql(sql)
        return self.conn.table(table_name=pydantic_model.table_name)
