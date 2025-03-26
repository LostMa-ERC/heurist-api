import duckdb
import pandas as pd
import unittest

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from heurist.converters.detail_converter import RecordDetailConverter


TIMESTAMP = {
    "dty_ID": 1,
    "value": {
        "timestamp": {"in": "1188", "type": "s", "circa": True},
        "comment": "1188",
        "estMinDate": 1188,
        "estMaxDate": 1188,
    },
}

SIMPLE = {
    "dty_ID": 1,
    "value": "2024-03-19",
}

COMPOUND = {
    "dty_ID": 1,
    "value": {
        "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        "end": {"latest": "1250", "earliest": "1246", "profile": "3"},
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
}

# Single simple date
d1 = {
    "date_of_creation": RecordDetailConverter.date(SIMPLE),
    "date_of_creation_TEMPORAL": RecordDetailConverter.temporal(SIMPLE),
}
# Timestamp from a repeatable date field
d2 = {
    "date_of_creation": RecordDetailConverter.date(TIMESTAMP),
    "date_of_creation_TEMPORAL": RecordDetailConverter.temporal(TIMESTAMP),
}
# Compound date
d3 = {
    "date_of_creation": RecordDetailConverter.date(COMPOUND),
    "date_of_creation_TEMPORAL": RecordDetailConverter.temporal(COMPOUND),
}


class PydanticModel(BaseModel):
    date_of_creation: List[Optional[datetime]] = Field(default=[])
    date_of_creation_TEMPORAL: Optional[dict] = Field(default=None)


class TemporalTest(unittest.TestCase):
    def setUp(self):
        self.conn = duckdb.connect()
        return super().setUp()

    def test(self):
        # Set up mixed temporal object data
        models = [
            PydanticModel.model_validate(d1),
            PydanticModel.model_validate(d2),
            PydanticModel.model_validate(d3),
        ]

        # Confirm that pandas models the temporal data as objects
        df = pd.DataFrame([m.model_dump() for m in models])
        column_type = df.date_of_creation_TEMPORAL.dtype
        self.assertEqual(column_type, "object")

        # Convert the pandas dataframe to a DuckDB table
        self.conn.sql("CREATE TABLE test AS FROM df")

        second_column = self.conn.table("test").description[1]
        column_type = second_column[1]
        # Assert that DuckDB parsed the temporal objects as dicts
        self.assertEqual(column_type, "dict")


if __name__ == "__main__":
    unittest.main()
