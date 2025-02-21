from pathlib import Path

import duckdb

SCHEMA_QUERY_FILEPATH = Path(__file__).parent.joinpath("selectRecSchema.sql")


with open(SCHEMA_QUERY_FILEPATH) as f:
    SCHEMA_QUERY = f.read()


def output_dicts(rel: duckdb.DuckDBPyRelation) -> list[dict]:
    output = []
    for row in rel.fetchall():
        output.append({k: v for k, v in zip(rel.columns, row)})
    return output
