import duckdb


def rel_to_dict_array(rel: duckdb.DuckDBPyRelation) -> list[dict]:
    output = []
    for row in rel.fetchall():
        output.append({k: v for k, v in zip(rel.columns, row)})
    return output
