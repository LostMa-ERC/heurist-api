from duckdb import DuckDBPyRelation
from lxml import etree

from heurist.doc.html.constants import TABLE_ROW_COLUMNS


class THead:
    def __init__(self, rel: DuckDBPyRelation, react_bootstrap: bool = False) -> None:
        self.rel = rel
        self.react_bootstrap = react_bootstrap
        self.rty_ID = rel.select("rty_ID").limit(1).fetchone()[0]

    def build_header(self) -> etree.Element:
        thead = etree.Element("thead", **{"class": "table-light sticky-header"})
        tr = self.build_row()
        thead.append(tr)
        return thead

    def add_columns(self, tr: etree.Element) -> None:
        for col in TABLE_ROW_COLUMNS:
            th = etree.SubElement(tr, "th", **{"scope": "col"})
            th.text = col

    def build_row(self) -> etree.Element:
        tr = etree.Element("tr")
        self.add_columns(tr=tr)
        return tr
