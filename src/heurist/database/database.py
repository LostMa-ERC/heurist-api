import pandas as pd
from duckdb import DuckDBPyConnection, DuckDBPyRelation
from heurist.database.basedb import HeuristDatabase
from heurist.models.dynamic import HeuristRecord
from heurist.sql import RECORD_BY_GROUP_TYPE, RECORD_TYPE_METADATA
from heurist.validators.record_validator import RecordValidator


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
    ) -> None:
        super().__init__(hml_xml, conn, db)

        # Create an empty index of targeted record types' Pydantic models
        self.pydantic_models = {}

        # Joining together the Heurist database's structural tables, construct an SQL
        # statement that selects the ID and name of the record types that belong to one
        # of the targeted record type groups
        condition = "\nWHERE rtg.rtg_Name like '{}'".format(record_type_groups[0])
        if len(record_type_groups) > 1:
            for rtg in record_type_groups[1:]:
                condition += " OR rtg.rtg_Name like '{}'".format(rtg)
        query = RECORD_BY_GROUP_TYPE + condition

        # Iterate through each targeted record type's ID and name
        for rty_ID, rty_Name in self.conn.sql(query).fetchall():
            # Using the ID, select the metadata of a record type's data fields (details)
            rel = self.conn.sql(query=RECORD_TYPE_METADATA, params=[rty_ID])
            # Using this metadata, create a dynamic Pydantic model for the record type
            data_field_metadata = rel.pl().to_dicts()
            model = HeuristRecord(
                rty_ID=rty_ID,
                rty_Name=rty_Name,
                detail_metadata=data_field_metadata,
            )
            # Add the dynamic Pydantic model to the index of models
            self.pydantic_models.update({rty_ID: model})

    def insert_records(
        self, record_type_id: int, records: list[dict]
    ) -> DuckDBPyRelation | None:
        # From the index of Pydantic models, get this record type's
        # dynamically-created Pydantic model.
        dynamic_model = self.pydantic_models[record_type_id].model
        table_name = self.pydantic_models[record_type_id].table_name

        # Prepare a list in which to store dictionaries of the validated record data.
        model_dict_sequence = []

        # Using the dynamically-created Pyandtic model, validate the metadata of
        # all the records of this type.
        validator = RecordValidator(
            pydantic_model=dynamic_model,
            records=records,
            rty_ID=record_type_id,
        )
        for model in validator:
            # Dump the validated record's data model to a dictionary.
            model_dict = model.model_dump(by_alias=True)
            # Add the dictionary representation of the validated data to the sequence.
            model_dict_sequence.append(model_dict)

        # If no records of this type have been created yet, skip it.
        if len(model_dict_sequence) == 0:
            return

        # Transform the sequence of dictionaries into a Pandas dataframe
        try:
            df = pd.DataFrame(model_dict_sequence)
            assert df.shape[1] > 0
        except Exception as e:
            from pprint import pprint

            pprint(model_dict_sequence)
            print(df)
            print(records)
            print(table_name)
            raise e

        # Delete any existing table for this record type.
        self.delete_existing_table(table_name=table_name)

        # From the dataframe, build a new table for the record type.
        sql = f"""CREATE TABLE {table_name} AS FROM df"""
        self.conn.sql(sql)
        return self.conn.table(table_name=table_name)
