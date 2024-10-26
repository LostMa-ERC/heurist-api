from dataclasses import dataclass

from lxml import etree

from heurist.doc.html.utils import escape_escape_characters, build_element_with_text

BASE = """
<!doctype html>
<html lang="en">
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"></link>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<title>LostMa Record Types</title>
</head>
<body>
<h1>LostMa Record Types</h1>
</body>
</html>
"""


@dataclass
class DataField:
    sec: str | None
    rst_DisplayName: str
    rst_DetailTypeID: str
    dty_HelpText: str | None
    dty_SemanticReferenceURL: str | None
    rst_RequirementType: str
    dty_Type: str
    dty_PtrTargetRectypeIDs: str | None
    dty_TermIDTreeNonSelectableIDs: str | None

    @staticmethod
    def column_names() -> list:
        return [
            "Section",
            "Name",
            "Field ID",
            "Help Text",
            "Semantic Reference URL",
            "Requirement",
            "Data Type",
            "Linked Record Types",
            "Vocabulary",
        ]

    @classmethod
    def load_from_row(cls, row: list):
        values = [escape_escape_characters(r) for r in row]
        return DataField(*values)

    def format_reference_url(self):
        if not self.dty_SemanticReferenceURL:
            return etree.fromstring("<td/>")
        else:
            a = f'<a class="link" target="_blank" rel="noreferrer noopener" href="{self.dty_SemanticReferenceURL}">{self.dty_SemanticReferenceURL}</a>'
            return etree.fromstring(f"<td>{a}</td>")

    def format_requirement_type(self):
        s = '<span class="badge badge-{}">{}</span>'
        name = self.rst_RequirementType.capitalize()
        if self.rst_RequirementType == "required":
            badge = "success"
        elif self.rst_RequirementType == "recommended":
            badge = "primary"
        elif self.rst_RequirementType == "optional":
            badge = "secondary"
        elif self.rst_RequirementType == "forbidden":
            badge = "dark"
            name = "Outmoded"
        return etree.fromstring(f"<td>{s.format(badge, name)}</td>")

    def format_target_record_types(
        self, present_records: list, record_name_index: dict
    ):
        if not self.dty_PtrTargetRectypeIDs:
            return etree.fromstring("<td/>")
        if self.dty_PtrTargetRectypeIDs:
            l = []
            for i in sorted([int(x) for x in self.dty_PtrTargetRectypeIDs.split("|")]):
                name = record_name_index[i]
                if i in present_records:
                    l.append(f'<a class="link" href="#{i}">{name}</a>')
                else:
                    l.append(name)
            s = f'<td>{", ".join(l)}</td>'
            return etree.fromstring(s)

    def format_term_ids(self):
        return etree.fromstring("<td/>")

    def format_data_type(self):
        name = self.dty_Type.capitalize()
        if self.dty_Type == "enum":
            name = "Vocabulary"
        elif self.dty_Type == "freetext" or self.dty_Type == "blocktext":
            name = "Text"
        elif self.dty_Type == "resource":
            name = "Foreign key"
        return etree.fromstring(f"<td>{name}</td>")

    def format_help_text(self):
        return build_element_with_text("td", self.dty_HelpText)

    def transform_non_section_fields(
        self, present_records: list, record_name_index: dict
    ) -> list[etree.Element]:
        return [
            etree.fromstring(f"<td>{self.rst_DisplayName}</td>"),
            etree.fromstring(f"<td>{self.rst_DetailTypeID}</td>"),
            self.format_help_text(),
            self.format_reference_url(),
            self.format_requirement_type(),
            self.format_data_type(),
            self.format_target_record_types(
                present_records=present_records, record_name_index=record_name_index
            ),
            self.format_term_ids(),
        ]

    def build_tr(self):
        tr = etree.Element("tr", **{"class": "table-light"})
        return tr

    def convert_n_row(
        self, record_name_index: dict, present_records: list
    ) -> etree.Element:
        tr = self.build_tr()
        for td in self.transform_non_section_fields(
            present_records=present_records, record_name_index=record_name_index
        ):
            tr.append(td)
        return tr

    def convert_to_first_row(
        self, rowspan: int, record_name_index: dict, present_records: list
    ) -> etree.Element:
        tr = self.build_tr()
        sec = f'<th scope="row" rowspan="{rowspan}">{self.sec}</th>'
        sec = etree.fromstring(sec)
        tr.append(sec)

        for td in self.transform_non_section_fields(
            present_records=present_records, record_name_index=record_name_index
        ):
            tr.append(td)

        return tr
