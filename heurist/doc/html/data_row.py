from lxml import etree
from dataclasses import dataclass
import duckdb
from heurist.doc.html.constants import BootstrapButton, CollapseDiv
from typing import Any


@dataclass
class TableRowData:
    sec: str | None
    rst_DisplayName: str
    rst_DetailTypeID: str
    dty_HelpText: str | None
    dty_SemanticReferenceURL: str | None
    rst_RequirementType: str
    dty_Type: str
    dty_PtrTargetRectypeIDs: str | None
    trm_TreeID: int | None
    trm_Label: str | None
    trm_Description: str | None
    vocabTerms: dict

    @classmethod
    def load_args(cls, *args) -> "TableRowData":
        values = []
        for a in args:
            if isinstance(a, str) or isinstance(a, int):
                values.append(cls.escape_escape_characters(a))
            elif isinstance(a, dict):
                clean_dict = {}
                ks, vs = a["key"], a["value"]
                d = {k: v for k, v in zip(ks, vs)}
                for k, v in d.items():
                    k = cls.escape_escape_characters(k)
                    if not isinstance(v, dict):
                        v = cls.escape_escape_characters(v)
                    else:
                        v = {
                            kk: cls.escape_escape_characters(vv) for kk, vv in v.items()
                        }
                    clean_dict.update({k: v})
                values.append(clean_dict)
            else:
                values.append(a)
        return TableRowData(*values)

    @staticmethod
    def escape_escape_characters(s: Any | None) -> str | None:
        if s:
            s = str(s)
            s = s.replace(r"\"", '"')
            s = s.replace(r"\'", "'")
            s = s.replace(r"\n", "\n")
            s = s.replace("<br>", "<br/>")
            return s


class SectionBlock:
    def __init__(self, section: str, rel: duckdb.DuckDBPyRelation) -> None:
        cols = TableRowData.__annotations__
        self.block = rel.filter(f"sec LIKE '{section}'").select(", ".join(cols))
        rows = []
        for row in self.block.fetchall():
            trd = TableRowData.load_args(*row)
            rows.append(trd)
        self.len = len(rows)
        self.first_row = rows.pop(0)
        if self.len == 1:
            self.rows = []
        else:
            self.rows = rows


class TableRow:
    bad_href = 'target="_blank"'
    good_href = 'target="_blank" rel="noreferrer noopener"'

    def __init__(
        self,
        row: TableRowData,
        present_records: list,
        record_name_index: dict,
        react_bootstrap: bool,
    ) -> None:
        if not row:
            raise ValueError("Must be given row data")
        self.row = row
        self.tr = etree.Element("tr", **{"class": "table-light"})
        self.present_records = present_records
        self.record_name_index = record_name_index
        self.react_bootstrap = react_bootstrap

    def build_first_row(self, rowspan: int | None = None) -> None:
        # Section
        th = self.set_section(rowspan=rowspan)
        self.tr.append(th)
        self.build_main_columns()
        return self.tr

    def build_main_columns(self) -> None:
        # Name
        self.tr.append(self.name)
        # Field ID
        self.tr.append(self.field_id)
        # Help Text
        self.tr.append(self.help_text)
        # Semantic Reference URL
        self.tr.append(self.reference_url)
        # Requirement
        self.tr.append(self.requirement_type)
        # Data Type
        self.tr.append(self.data_type)
        # Linked Record Types
        self.tr.append(self.linked_record_types)
        # Vocabulary
        self.tr.append(self.vocab_terms)
        return self.tr

    def set_section(self, rowspan: int) -> etree.Element:
        th = etree.SubElement(
            self.tr,
            "th",
            **{"scope": "row", "rowspan": str(rowspan)},
        )
        th.text = self.row.sec
        return th

    @property
    def name(self) -> etree.Element:
        return etree.fromstring(f"<td>{self.row.rst_DisplayName}</td>")

    @property
    def field_id(self) -> etree.Element:
        return etree.fromstring(f"<td>{self.row.rst_DetailTypeID}</td>")

    @property
    def help_text(self) -> etree.Element:
        desc = self.row.dty_HelpText
        desc = desc.replace(self.bad_href, self.good_href)
        return etree.fromstring(f"<td>{desc}</td>")

    @property
    def reference_url(self) -> etree.Element:
        if not self.row.dty_SemanticReferenceURL:
            return etree.fromstring("<td/>")
        else:
            a = f'<a class="link" target="_blank" rel="noreferrer noopener" href="{self.row.dty_SemanticReferenceURL}">{self.row.dty_SemanticReferenceURL}</a>'
            return etree.fromstring(f"<td>{a}</td>")

    @property
    def requirement_type(self) -> etree.Element:
        s = '<span class="badge badge-{}">{}</span>'
        name = self.row.rst_RequirementType.capitalize()
        if self.row.rst_RequirementType == "required":
            badge = "success"
        elif self.row.rst_RequirementType == "recommended":
            badge = "primary"
        elif self.row.rst_RequirementType == "optional":
            badge = "secondary"
        elif self.row.rst_RequirementType == "forbidden":
            badge = "dark"
            name = "Outmoded"
        return etree.fromstring(f"<td>{s.format(badge, name)}</td>")

    @property
    def data_type(self) -> etree.Element:
        name = self.row.dty_Type.capitalize()
        if self.row.dty_Type == "enum":
            name = "Vocabulary"
        elif self.row.dty_Type == "freetext" or self.row.dty_Type == "blocktext":
            name = "Text"
        elif self.row.dty_Type == "resource":
            name = "Foreign key"
        return etree.fromstring(f"<td>{name}</td>")

    @property
    def linked_record_types(self) -> etree.Element:
        if not self.row.dty_PtrTargetRectypeIDs:
            return etree.fromstring("<td/>")
        if self.row.dty_PtrTargetRectypeIDs:
            l = []
            for i in sorted(
                [int(x) for x in self.row.dty_PtrTargetRectypeIDs.split("|")]
            ):
                name = self.record_name_index[i]
                if i in self.present_records:
                    l.append(f'<a class="link" href="#{i}">{name}</a>')
                else:
                    l.append(name)
            s = f'<td>{", ".join(l)}</td>'
            return etree.fromstring(s)

    @property
    def vocab_terms(self) -> etree.Element:
        if not self.row.vocabTerms:
            td = etree.fromstring("<td/>")
        else:
            td = etree.Element("td")
            tdiv = etree.SubElement(
                td,
                "div",
                **{"id": f"Vocab{self.row.rst_DetailTypeID}"},
            )
            p = etree.SubElement(tdiv, "p")
            p.text = self.row.trm_Label

            ul = etree.SubElement(
                tdiv,
                "ul",
                **{"class": "list-group list-group-flush"},
            )
            for term_label, term_details in self.row.vocabTerms.items():
                url = term_details["url"]
                description = term_details["description"]
                li = etree.SubElement(
                    ul,
                    "li",
                    **{
                        "class": "list-group-item list-group-item-light",
                        "id": term_details["id"],
                    },
                )
                ms2 = etree.SubElement(li, "div", **{"class": "ms-2 me-auto"})
                fw = etree.SubElement(ms2, "div")
                if url:
                    a = etree.SubElement(
                        fw,
                        "a",
                        **{
                            "class": "link",
                            "target": "_blank",
                            "rel": "noreferrer noopener",
                            "href": url,
                        },
                    )
                    a.text = term_label
                else:
                    fw.text = term_label
                if description:
                    desc = description.replace(self.bad_href, self.good_href)
                    div = etree.fromstring(
                        f'<small class="text-body-secondary">{desc}</small>'
                    )
                    ms2.append(div)

        return td
