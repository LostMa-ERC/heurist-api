from duckdb import DuckDBPyRelation
from lxml import etree

from heurist.doc.html.constants import DataField


class TBody:
    cols = ", ".join(DataField.__annotations__)

    def __init__(
        self, rel: DuckDBPyRelation, record_name_index: dict, present_records: list
    ) -> None:
        rel = rel.filter("dty_Type NOT LIKE 'separator'")
        sections = rel.aggregate("sec, min(rst_DisplayOrder) as m").order("m")
        self.sections = [t[0] for t in sections.fetchall()]
        self.fields = rel.select(self.cols)
        self.record_name_index = record_name_index
        self.present_records = present_records

    def build(self) -> etree.Element:
        tbody = etree.Element("tbody")

        for sec in self.sections:
            fields_in_section = [
                DataField.load_from_row(r)
                for r in self.fields.filter(f"sec LIKE '{sec}'")
                .select(self.cols)
                .fetchall()
            ]
            rowspan = len(fields_in_section)
            tr = fields_in_section[0].convert_to_first_row(
                rowspan=rowspan,
                record_name_index=self.record_name_index,
                present_records=self.present_records,
            )
            tbody.append(tr)
            for row in fields_in_section[1:]:
                tr = row.convert_n_row(
                    record_name_index=self.record_name_index,
                    present_records=self.present_records,
                )
                tbody.append(tr)

        return tbody
