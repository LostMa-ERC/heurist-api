import json
from datetime import date
from pathlib import Path

import duckdb
from heurist.schema.rel_to_dict import convert_rty_description
from heurist.sql.sql_safety import SafeSQLName


def output_csv(dir: Path, descriptions: list[duckdb.DuckDBPyRelation]) -> None:
    for rel in descriptions:
        name = rel.select("rty_Name").limit(1).fetchone()[0]
        safe_name = SafeSQLName().create_table_name(name)
        fp = dir.joinpath(safe_name).with_suffix(".csv")
        rel.write_csv(file_name=str(fp), header=True)


def output_json(descriptions: list[duckdb.DuckDBPyRelation], fp: Path) -> None:
    date_string = date.today().isoformat()
    data = {"lastModified": date_string, "items": []}
    for desc in descriptions:
        kv_dict = convert_rty_description(description=desc)
        for id, metadata in kv_dict.items():
            d = {"id": id} | metadata
            data["items"].append(d)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
