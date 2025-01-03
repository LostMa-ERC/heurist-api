import polars as pl
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from pydantic import BaseModel

from heurist.components.database.duckbase import DuckBase
from heurist.components.heurist.convert_record_detail import HeuristRecordDetail
from heurist.components.sql_models.record_details import RecordTypeModeler
from heurist.components.sql_models.select_record_structure import QUERY


class Database(DuckBase):
    def __init__(
        self,
        hml_xml: bytes,
        conn: DuckDBPyConnection | None = None,
        save_structure: bool = False,
        db: str | None = ":memory:",
        record_type_groups: list[str] = ["My record types"],
    ) -> None:
        super().__init__(hml_xml, conn, db, save_structure)

        self.managers_record_type = {
            r.rty_ID: r for r in self.yield_record_details(record_type_groups)
        }

    def describe_record_fields(self, rty_ID: int) -> DuckDBPyRelation:
        """Join the detail, record structure, and record type tables for a specific
        record type and add the label and description of the last section / separator
        preceding the detail.

        Args:
            rty_ID (int): ID of the targeted record.

        Returns:
            DuckDBPyRelation: A DuckDB Python relation that can be queried or converted.
        """
        return self.conn.from_query(query=QUERY, params=[rty_ID])

    def model_record_data(
        self, record_manager: RecordTypeModeler, records: list[dict]
    ) -> list[BaseModel]:
        """Model the data of each record in a list of records.

        Args:
            record_type_id (int): ID of the type of record targeted for processing.
            records (list[dict]): A list of raw JSON records.

        Yields:
            Iterator[BaseModel]: _description_
        """

        modeled_records = []
        DetailConverter = HeuristRecordDetail()

        for record in records:
            # Skip any records in the data set that are not targeted
            if record["rec_RecTypeID"] != str(record_manager.rty_ID):
                continue

            # Flatten the detail JSON into a simple key-value dict
            flat_details = {}
            for detail in DetailConverter(record["details"]):
                flat_details.update(detail)

            # Add in generic metadata for the record
            flat_details.update(
                {"rec_ID": record["rec_ID"], "rec_RecTypeID": record["rec_RecTypeID"]}
            )

            # Validate the flattened details inside the record type's Pydantic model
            try:
                modeled_records.append(
                    record_manager.model.model_validate(flat_details)
                )
            except Exception as e:
                from pprint import pprint

                pprint(flat_details)
                raise e

        # Return a list of validated Pydantic models
        return modeled_records

    def insert_records(
        self, record_type_id: int, records: list[dict]
    ) -> DuckDBPyRelation:
        """_summary_

        Args:
            record_type_id (int): _description_
            records (list[dict]): _description_

        Returns:
            DuckDBPyRelation: _description_
        """

        # Given the record type's ID, get the SQL-safe table name for the type
        record_manager = self.managers_record_type[record_type_id]

        # Model all the records' data
        modeled_records = self.model_record_data(record_manager, records)
        if len(modeled_records) == 0:
            return
        else:
            modeled_dicts = [m.model_dump(by_alias=True) for m in modeled_records]

        # Transform the series of models into a dataframe
        df = pl.from_dicts(modeled_dicts, infer_schema_length=None)

        # Delete any existing table
        self.delete_existing_table(table_name=record_manager.table_name)

        # From the dataframe, build a table for the record type
        sql = f"""CREATE TABLE {record_manager.table_name} AS FROM df"""
        self.conn.sql(sql)
        return self.conn.table(table_name=record_manager.table_name)
