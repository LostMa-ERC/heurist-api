from pathlib import Path

from heurist.components.database.database import Database
from heurist.components.sql_models.sql_safety import SafeSQLName
from heurist.doc.html import Doc


def output_csv(db: Database, dir: Path, id: str):
    rel = db.describe_record_fields(id)
    name = rel.aggregate("rty_Name").fetchone()[0]
    safe_name = SafeSQLName().create_table_name(name)
    fp = dir.joinpath(safe_name).with_suffix(".csv")
    rel.write_csv(file_name=str(fp), header=True)


def output_html(record_types: list, dir: Path, db: Database):
    fp = dir.joinpath("recordTypes.html")
    doc = Doc()
    for rty in record_types:
        rel = db.describe_record_fields(rty_ID=rty)
