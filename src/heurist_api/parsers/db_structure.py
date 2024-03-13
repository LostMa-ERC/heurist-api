from lxml import etree
from pathlib import Path
from typing import List

import re

from dataclasses import dataclass, field


@dataclass
class Field:
    detail_ID: int
    name: str
    type: str
    required: bool
    repeats: bool = False
    sql_safe_name: str = ""
    value: str | None = None

    def __post_init__(self):
        if self.type == "enum":
            self.repeats = True
        self.sql_safe_name = self.make_name_sql_safe(self.name)

    @classmethod
    def make_name_sql_safe(cls, name: str):
        no_parentheses = re.sub(r"\(.\)", "", name)
        no_non_letters = re.sub(r"\W", "_", no_parentheses)
        return no_non_letters.lower()

    def __repr__(self) -> str:
        dtype = "VARCHAR"
        if self.repeats:
            dtype = "VARCHAR[]"

        s = "%s %s" % (self.sql_safe_name, dtype)

        if self.required:
            s += "IS NOT NULL"
        return s


@dataclass
class Table:
    name: str
    record_id: int
    fields: List = field(default_factory=list)

    @property
    def fieldnames(self) -> List[str]:
        return [f.name for f in self.fields]


class DBStructure:
    def __init__(self, db_xml: Path) -> None:
        self.tree = etree.parse(db_xml)
        self.header_details = []

        for dty_Name in self.tree.xpath(".//dty_Name[contains(text(), 'Header')]"):
            dty = dty_Name.getparent()
            dty_ID = dty.find("dty_ID")
            self.header_details.append(dty_ID.text)

    def build_table(self, rst_ID: int, name: str):
        table = Table(name=name, record_id=rst_ID)

        details = []

        # Collect detail data from the Record Type Structure list (rst)
        for rst_RecTypeID in self.tree.xpath(
            ".//rst_RecTypeID[contains(text(), '{}')]".format(rst_ID)
        ):
            rst = rst_RecTypeID.getparent()
            rst_DetailTypeID = rst.find("rst_DetailTypeID").text

            # If the detail is not a header, append its data
            if rst_DetailTypeID not in self.header_details:
                if rst.find("rst_RequirementType").text == "required":
                    required = True
                else:
                    required = False
                display_order = rst.find("rst_DisplayOrder").text
                details.append((rst_DetailTypeID, required, display_order))

        fields = []

        for detail_id, required, display_order in details:
            dty_id = self.tree.xpath(
                ".//dty_ID[contains(text(), '{}')]".format(detail_id)
            )[0]
            dty = dty_id.getparent()
            dty_Name = dty.find("dty_NameInOriginatingDB").text
            dty_Type = dty.find("dty_Type").text
            field = Field(
                detail_ID=detail_id, name=dty_Name, type=dty_Type, required=required
            )
            fields.append((display_order, field))

        fields = sorted(fields, key=lambda tup: tup[0])
        table.fields = [f for _, f in fields]

        return table
