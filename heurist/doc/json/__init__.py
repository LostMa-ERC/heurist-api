import json
from pathlib import Path

import duckdb

from heurist.doc.json.converter import convert_rty_description


def output_json(descriptions: list[duckdb.DuckDBPyRelation], fp: Path) -> None:
    data = {}
    for desc in descriptions:
        d = convert_rty_description(description=desc)
        data.update(d)

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
