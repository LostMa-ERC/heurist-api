from lxml import etree
from pathlib import Path
from typing import Dict, Generator
import csv


from heurist_api.constants import NS
from heurist_api.parsers.db_structure import Table


class RecordParser:
    def __init__(self, record_xml: Path, table: Table, output: Path) -> None:
        self.tree = etree.parse(record_xml)
        self.table = table
        self.field_index = {f.detail_ID: f for f in table.fields}
        query = self.tree.find("hml:query", namespaces=NS)
        self.record_type_id = query.get("q").split(":")[-1]
        self.outfile = output.joinpath(f"{table.name}_RecID-{self.record_type_id}.csv")

    def pivoter(self) -> Generator[Dict | None, None, None]:
        for record in self.tree.xpath(".//hml:record", namespaces=NS):

            row = {}

            record_type_id = record.find("hml:type", namespaces=NS).attrib["id"]
            if record_type_id != self.record_type_id:
                continue

            record_id = record.find("hml:id", namespaces=NS).text
            row.update({"record H-ID": record_id})

            for detail in record.xpath("hml:detail", namespaces=NS):
                detail_type_id = detail.attrib["id"]
                field = self.field_index.get(detail_type_id)
                if field:
                    row.update({field.name: detail.text})

            yield row

    def convert(self):
        output = self.outfile
        with open(output, "w") as f:
            writer = csv.DictWriter(f, ["record H-ID"] + list(self.table.fieldnames))
            writer.writeheader()
            for record in self.pivoter():
                if record:
                    writer.writerow(record)
