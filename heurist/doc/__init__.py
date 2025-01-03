import json
from pathlib import Path

import duckdb

from heurist.components.sql_models.sql_safety import SafeSQLName
from heurist.doc.json_tools.converter import convert_rty_description


def output_csv(dir: Path, descriptions: list[duckdb.DuckDBPyRelation]) -> None:
    for rel in descriptions:
        name = rel.select("rty_Name").limit(1).fetchone()[0]
        safe_name = SafeSQLName().create_table_name(name)
        fp = dir.joinpath(safe_name).with_suffix(".csv")
        rel.write_csv(file_name=str(fp), header=True)


def output_json(descriptions: list[duckdb.DuckDBPyRelation], fp: Path) -> None:
    data = {}
    for desc in descriptions:
        d = convert_rty_description(description=desc)
        data.update(d)

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
