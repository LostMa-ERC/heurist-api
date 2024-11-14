from pathlib import Path

from duckdb import DuckDBPyRelation
from lxml import etree

from heurist.doc.html.constants import BASE
from heurist.doc.html.header import Header
from heurist.doc.html.thead import THead
from heurist.doc.html.tbody import TBody


class Doc:
    def __init__(self, record_name_index: dict, present_records: list) -> None:
        self.root = etree.HTML(BASE)
        self.body = self.root.find("body")
        self.record_name_index = record_name_index
        self.present_records = present_records

    @property
    def indented_html(self) -> str:
        etree.indent(self.root)
        return etree.tostring(self.root, pretty_print=True).decode()

    def write(self, fp: Path) -> None:
        with open(fp, "w") as f:
            f.write(self.indented_html)

    def build_record(
        self, rel: DuckDBPyRelation, react_bootstrap: bool = False
    ) -> etree.Element:
        # Add container for the record type to the page's body
        rty_ID = rel.select("rty_ID").limit(1).fetchone()[0]
        div = etree.Element(
            "div", **{"class": "container-fluid recordTypeProfile", "id": str(rty_ID)}
        )

        # Header that describes the record type
        header = Header(rel=rel)
        div.append(header.root)

        # Table container
        container = etree.SubElement(div, "div", **{"class": "container-fluid ml-1"})
        table_container = etree.SubElement(
            container, "div", **{"class": "table-responsive"}
        )
        table = etree.SubElement(
            table_container, "table", **{"class": "table table-bordered"}
        )

        # First row of the table, column headers
        thead = THead(rel=rel, react_bootstrap=react_bootstrap).build_header()
        table.append(thead)

        # Remaining rows
        tbody = TBody(
            rel=rel.order("rst_DisplayOrder"),
            record_name_index=self.record_name_index,
            present_records=self.present_records,
        ).build(react_bootstrap=react_bootstrap)
        table.append(tbody)

        # Return the container
        return div

    def add_record(self, rel: DuckDBPyRelation) -> None:
        record_container = self.build_record(rel=rel)
        self.body.append(record_container)
