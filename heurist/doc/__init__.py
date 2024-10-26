from pathlib import Path

from heurist.components.database.database import Database
from heurist.components.sql_models.sql_safety import SafeSQLName
from heurist.doc.html import Doc
from heurist.doc.js import JavaScriptOutput


def output_csv(db: Database, dir: Path, id: str):
    rel = db.describe_record_fields(id)
    name = rel.select("rty_Name").limit(1).fetchone()[0]
    safe_name = SafeSQLName().create_table_name(name)
    fp = dir.joinpath(safe_name).with_suffix(".csv")
    rel.write_csv(file_name=str(fp), header=True)


class OutputHtml:
    def __init__(self, db: Database, record_types: list) -> None:
        self.db = db
        self.present_records = record_types
        self.record_name_index = {
            t[0]: t[1]
            for t in db.conn.table("rty")
            .select("rty_ID, rty_Name")
            .order("rty_Name")
            .fetchall()
        }
        self.doc = Doc(
            record_name_index=self.record_name_index, present_records=record_types
        )

    def __call__(self, rty_ID: int):
        rel = self.db.describe_record_fields(rty_ID=rty_ID)
        self.doc.add_record(rel)

    def write(self, fp: Path):
        self.doc.write(fp)
