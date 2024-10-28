import re
from pathlib import Path

from lxml import etree

from heurist.components.database.database import Database
from heurist.components.sql_models.sql_safety import SafeSQLName
from heurist.doc.html import Doc
from heurist.doc.html.constants import Collapse, AriaExpanded, OnClick
from heurist.doc.js.constants import (
    BASE,
    REACT_USE_STATE,
    REACT_IMPORT,
    HASHROUTER_IMPORT,
)


class JavaScriptOutput:
    def __init__(
        self,
        dir: Path,
        db: Database,
        record_types: list,
        react_hash_router: bool = False,
    ) -> None:
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
        self.react_hash_router = react_hash_router

    @staticmethod
    def change_to_hashlink(s: str) -> str:
        """_summary_

        Examples:
            >>> s = '<td><a className="link" href="#102">storyverse</a></td><td><a className="link" href="#103">story</a></td>'
            >>> JavaScriptOutput.change_to_hashlink(s)
            '<td><HashLink to="#102">storyverse</HashLink></td><td><HashLink to="#103">story</HashLink></td>'

        Args:
            s (str): _description_

        Returns:
            str: _description_
        """

        pattern = re.compile(r'<a className="link" href=("#\w+")>(\w+)<\/a>')
        repl = "<HashLink to=\\1>\\2</HashLink>"
        return re.sub(pattern=pattern, repl=repl, string=s)

    @staticmethod
    def convert_classname(s: str) -> str:
        """_summary_
        style="font-size:24px;text-transform:uppercase">
        style={{fontSize: "24px", textTransform: "uppercase"}}

        Args:
            s (str): _description_

        Returns:
            str: _description_
        """

        # Replace class with className
        s = s.replace("class=", "className=")

        # Replace styling with jsx version
        fixed_card_styling = 'style="position: sticky;top: 0"'
        jsx_styling = r'style={{position: "sticky", top: "0"}}'
        s = s.replace(fixed_card_styling, jsx_styling)
        return s

    @staticmethod
    def convert_react_button(s: str) -> str:
        # Replace stand-ins for button with JavaScript
        pattern = OnClick.placeholder
        repl = OnClick.real
        s = s.replace(pattern, repl)

        pattern = AriaExpanded.placeholder
        repl = AriaExpanded.real
        s = s.replace(pattern, repl)

        pattern = Collapse.placeholder
        repl = Collapse.real
        s = s.replace(pattern, repl)

        return s

    def __call__(self, rty_ID: int):
        # Join the database's information into a record type description
        rel = self.db.describe_record_fields(rty_ID=rty_ID)

        # Convert the record type name into Pascal case
        name = rel.select("rty_Name").limit(1).fetchone()[0]
        component_name = SafeSQLName().create_table_name(name)

        # Convert the information into an HTML block
        elem = self.doc.build_record(rel=rel, react_bootstrap=self.react_hash_router)
        etree.indent(elem)
        html_string = etree.tostring(element_or_tree=elem).decode()

        # Replace class with className
        clean_string = self.convert_classname(html_string)
        imports = ""
        js_script = ""

        # Replace placeholders for React App / Bootstrap modules
        if self.react_hash_router:
            # Change hash router
            clean_hash_router_string = self.change_to_hashlink(clean_string)
            if clean_string != clean_hash_router_string:
                imports += HASHROUTER_IMPORT
                clean_string = clean_hash_router_string
            # Change react button attributes
            clean_react_button_string = self.convert_react_button(clean_string)
            if clean_string != clean_react_button_string:
                imports += REACT_IMPORT
                clean_string = clean_react_button_string
                js_script = REACT_USE_STATE

        jsx = BASE.format(
            function_name=component_name,
            html_block=clean_string,
            imports=imports,
            js_script=js_script,
        )

        fp = self.dir.joinpath(f"{component_name}.js")
        with open(fp, "w") as f:
            f.write(jsx)
