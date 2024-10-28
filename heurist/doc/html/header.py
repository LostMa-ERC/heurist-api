from lxml import etree
from duckdb import DuckDBPyRelation
from heurist.doc.html.utils import escape_escape_characters, build_element_with_text


class Header:
    def __init__(self, rel: DuckDBPyRelation):
        self.df = rel
        self.root = etree.Element(
            "div",
            **{
                "class": "card bg-light mb-3",
                # "style": "position: sticky;top: 0",
            },
        )
        self.body = etree.SubElement(self.root, "div", **{"class": "card-body"})
        self.build()

    @property
    def record_name(self) -> str:
        return self.df.select("rty_Name").limit(1).fetchone()[0]

    @property
    def record_id(self) -> int:
        return self.df.select("rty_ID").limit(1).fetchone()[0]

    @property
    def record_description(self) -> str | None:
        s = self.df.select("rty_Description").limit(1).fetchone()[0]
        return escape_escape_characters(s)

    @property
    def record_reference(self) -> str | None:
        return self.df.select("rty_ReferenceURL").limit(1).fetchone()[0]

    def build(self):
        h5 = etree.SubElement(self.body, "h4", **{"class": "card-title"})
        h5.text = self.record_name

        h6 = etree.SubElement(
            self.body, "h6", **{"class": "card-subtitle mb-2 text-body-secondary"}
        )
        h6.text = f"Record ID {self.record_id}"

        p = build_element_with_text("p", text=self.record_description, cls="card-text")
        self.body.append(p)
