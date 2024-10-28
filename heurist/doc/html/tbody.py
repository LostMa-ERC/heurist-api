from duckdb import DuckDBPyRelation
from lxml import etree

from heurist.doc.html.data_row import SectionBlock, TableRow


class TBody:

    def __init__(
        self,
        rel: DuckDBPyRelation,
        record_name_index: dict,
        present_records: list,
    ) -> None:
        self.record_name_index = record_name_index
        self.present_records = present_records
        self.rel = rel.filter("dty_Type NOT LIKE 'separator'")
        self.sections = [
            t[0]
            for t in self.rel.aggregate("sec, min(rst_DisplayOrder) as m")
            .order("m")
            .fetchall()
        ]
        self.rty_ID = rel.select("rty_ID").limit(1).fetchone()[0]

    def build(self, react_bootstrap: bool = False) -> etree.Element:
        tbody = etree.Element("tbody")

        for sec in self.sections:
            sb = SectionBlock(section=sec, rel=self.rel)

            # First row
            tr = TableRow(
                row=sb.first_row,
                record_name_index=self.record_name_index,
                present_records=self.present_records,
                react_bootstrap=react_bootstrap,
            )
            tr = tr.build_first_row(rowspan=sb.len)
            tbody.append(tr)

            # Other rows
            for row in sb.rows:
                tr = TableRow(
                    row=row,
                    record_name_index=self.record_name_index,
                    present_records=self.present_records,
                    react_bootstrap=react_bootstrap,
                )
                tr = tr.build_main_columns()
                tbody.append(tr)

        return tbody
