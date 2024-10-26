from duckdb import DuckDBPyRelation
from lxml import etree

from heurist.doc.html.constants import DataField


class THead:
    def __init__(self, rel: DuckDBPyRelation) -> None:
        self.rel = rel

    def build_header(self) -> etree.Element:
        thead = etree.Element("thead", **{"class": "table-light sticky-header"})
        tr = self.build_row()
        thead.append(tr)
        return thead

    def add_columns(self, tr: etree.Element) -> None:
        for col, id in zip(DataField.column_names(), DataField.__annotations__):
            th = etree.SubElement(tr, "th", **{"scope": "col", "data-field": id})
            th.text = col

    def build_row(self) -> etree.Element:
        tr = etree.Element("tr")
        self.add_columns(tr=tr)
        return tr
