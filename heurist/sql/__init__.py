from pathlib import Path

import duckdb

SCHEMA_QUERY_FILEPATH = Path(__file__).parent.joinpath("selectRecordTypeSchema.sql")
RECORD_BY_GROUP_TYPE_FILEPATH = Path(__file__).parent.joinpath(
    "joinRecordTypeIDNameByGroupType.sql"
)
RECORD_TYPE_METADATA_QUERY_FILEPATH = Path(__file__).parent.joinpath(
    "joinRecordTypeMetadata.sql"
)


with open(SCHEMA_QUERY_FILEPATH) as f:
    RECORD_TYPE_SCHEMA = f.read()

with open(RECORD_BY_GROUP_TYPE_FILEPATH) as f:
    RECORD_BY_GROUP_TYPE = f.read()

with open(RECORD_TYPE_METADATA_QUERY_FILEPATH) as f:
    RECORD_TYPE_METADATA = f.read()


def output_dicts(rel: duckdb.DuckDBPyRelation) -> list[dict]:
    output = []
    for row in rel.fetchall():
        output.append({k: v for k, v in zip(rel.columns, row)})
    return output
