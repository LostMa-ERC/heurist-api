from heurist import setup_logger, DATABASE_LOG

import pandas as pd
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pydantic import BaseModel

from heurist.database.basedb import HeuristDatabase
from heurist.converters.dynamic_record_type_modeler import (
    DynamicRecordTypeModel,
)
from heurist.converters.record_modeler import ModelValidationPrep

logger = setup_logger(name="validation", filepath=DATABASE_LOG)


class TransformedDatabase(HeuristDatabase):
    """Class for building and populating SQL tables with data collected and \
    transformed from remote Heurist DB.
    """

    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        db: str | None = ":memory:",
        record_type_groups: list[str] = ["My record types"],
        require_date_object: bool = False,
    ) -> None:
        super().__init__(hml_xml, conn, db)

        self.pydantic_models = {
            r.rty_ID: r for r in self.yield_record_details(record_type_groups)
        }
        self.require_date_objects = require_date_object

    def model_record_data(
        self, pydantic_model: DynamicRecordTypeModel, records: list[dict]
    ) -> list[BaseModel]:
        """Model the data of each record in a list of records.

        Args:
            pydantic_model (DynamicRecordTypeModel): Pydantic model created for the \
                record.
            records (list[dict]): A JSON array of a record's details.

        Yields:
            Iterator[BaseModel]: Array of Pydantic models validated with records' data.
        """

        modeled_records = []

        # Create a validation modeler for this record type
        validation_prep = ModelValidationPrep(
            pydantic_model=pydantic_model,
            require_date_object=self.require_date_objects,
            logger=logger,
        )

        for record in records:
            # Skip any records in the data set that are not targeted
            if record["rec_RecTypeID"] != str(pydantic_model.rty_ID):
                continue

            # Transform the record's details into a set of key-value pairs for
            # validation in a Pydantic model
            pydantic_validation_dict = validation_prep(record=record)

            # With the recorrd type's Pydantic model, validate the dictionary
            try:
                modeled_records.append(
                    pydantic_model.model.model_validate(pydantic_validation_dict)
                )
            except Exception as e:
                message = f"Record ID: {record['rec_ID']}\n\t{e}\n"
                logger.error(message)

        # Return a list of validated Pydantic models
        return modeled_records

    def insert_records(
        self, record_type_id: int, records: list[dict]
    ) -> DuckDBPyRelation | None:

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
