from heurist.doc.html import Doc
from lxml import etree
from heurist.components.sql_models.sql_safety import SafeSQLName
from heurist.doc.js.constants import BASE
from heurist.components.database.database import Database
from pathlib import Path


class JavaScriptOutput:
    def __init__(self, dir: Path, db: Database, record_types: list) -> None:
        self.dir = dir
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

    @staticmethod
    def convert_html_to_jsx(s: str) -> str:
        """_summary_
        style="font-size:24px;text-transform:uppercase">
        style={{fontSize: "24px", textTransform: "uppercase"}}

        Args:
            s (str): _description_

        Returns:
            str: _description_
        """

        s = s.replace("class=", "className=")
        fixed_card_styling = 'style="position: sticky;top: 0"'
        jsx_styling = r'style={{position: "sticky", top: "0"}}'
        s = s.replace(fixed_card_styling, jsx_styling)
        return s

    def __call__(self, rty_ID: int):
        # Join the database's information into a record type description
        rel = self.db.describe_record_fields(rty_ID=rty_ID)

        # Convert the record type name into Pascal case
        name = rel.select("rty_Name").limit(1).fetchone()[0]
        component_name = SafeSQLName().create_table_name(name)

        # Convert the information into an HTML block
        elem = self.doc.build_record(rel=rel)
        etree.indent(elem)
        html_string = etree.tostring(element_or_tree=elem).decode()

        js_string = BASE.format(function_name=component_name, html_block=html_string)
        clean_string = self.convert_html_to_jsx(js_string)

        fp = self.dir.joinpath(f"{component_name}.js")
        with open(fp, "w") as f:
            f.write(clean_string)
