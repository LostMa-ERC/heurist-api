import duckdb


def output_dicts(rel: duckdb.DuckDBPyRelation) -> list[dict]:
    output = []
    for row in rel.fetchall():
        output.append({k: v for k, v in zip(rel.columns, row)})
    return output
