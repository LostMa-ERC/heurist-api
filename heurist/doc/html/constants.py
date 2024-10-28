from dataclasses import dataclass


BASE = """
<!doctype html>
<html lang="en">
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://getbootstrap.com/docs/5.2/assets/css/docs.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
<title>LostMa Record Types</title>
</head>
<body>
<h1>LostMa Record Types</h1>
</body>
</html>
"""

TABLE_ROW_COLUMNS = [
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


@dataclass
class Collapse:
    placeholder = '<Collapse in="OPEN">'
    real = "<Collapse in={open}>"


@dataclass
class AriaExpanded:
    placeholder = 'aria-expanded="OPEN"'
    real = "aria-expanded={open}"


@dataclass
class OnClick:
    placeholder = 'onClick="SET_OPEN"'
    real = "onClick={() => setOpen(!open)}"


class BootstrapButton:
    def __init__(self) -> None:
        pass

    @classmethod
    def build(cls, div_id: int, text: str) -> str:
        """Produces the following with placeholders at JavaScript:

        <Button
        onClick={() => setOpen(!open)}
        aria-controls="example-collapse-text"
        aria-expanded={open}>
        text
        </Button>

        Args:
            div_id (int): _description_

        Returns:
            str: _description_
        """
        return f'<Button {OnClick.placeholder} aria-controls="{div_id}" {AriaExpanded.placeholder}>{text}</Button>'


class CollapseDiv:
    def __init__(self) -> None:
        pass

    @classmethod
    def build(cls, div_id: int, text: str) -> str:
        """Produces the following with placeholders at JavaScript:

        <Collapse in={open}>
            <div id="div_id">
            text
            </div>
        </Collapse>

        Args:
            div_id (int): _description_
            text (str): _description_

        Returns:
            str: _description_
        """

        return f'{Collapse.placeholder}<div id="{div_id}">{text}</div></Collapse>'


# @dataclass
# class DataField:
#     sec: str | None
#     rst_DisplayName: str
#     rst_DetailTypeID: str
#     dty_HelpText: str | None
#     dty_SemanticReferenceURL: str | None
#     rst_RequirementType: str
#     dty_Type: str
#     dty_PtrTargetRectypeIDs: str | None
#     trm_TreeID: int | None
#     trm_Label: str | None
#     trm_Description: str | None
#     vocabTerms: dict | None

#     @staticmethod
#     def column_names() -> list:
#         return [
#             "Section",
#             "Name",
#             "Field ID",
#             "Help Text",
#             "Semantic Reference URL",
#             "Requirement",
#             "Data Type",
#             "Linked Record Types",
#             "Vocabulary",
#         ]

#     @classmethod
#     def load_from_row(cls, row: list):
#         values = [escape_escape_characters(r) for r in row]
#         return DataField(*values)

#     def format_vocab_terms(self, react_bootstrap: bool, rty_ID: int):
#         if not self.vocabTerms:
#             return etree.fromstring("<td/>")
#         else:
#             vocab_dict = {
#                 k: v for k, v in zip(self.vocabTerms["key"], self.vocabTerms["value"])
#             }
#             td = etree.Element("td")
#             p = etree.SubElement(td, "p", {"id": self.trm_TreeID})
#             p.text = self.trm_Label
#             ul = etree.SubElement(td, "ul", **{"class": "list-group"})
#             for term_label, term_details in vocab_dict.items():
#                 term_label = escape_escape_characters(term_label)
#                 desc = escape_escape_characters(term_details["description"])
#                 url = term_details["url"]

#                 # Make a new line item for this term
#                 li = etree.SubElement(ul, "li", **{"class": "list-group-item"})

#                 # Simply list the term label
#                 if not desc and not url:
#                     li.text = term_label

#                 elif url:
#                     attrs = {
#                         "class": "link",
#                         "target": "_blank",
#                         "rel": "noreferrer noopener",
#                         "href": url,
#                     }
#                     a = etree.SubElement(li, "a", **attrs)
#                     a.text = term_label

#                 # If writing for a React app and there's a description,
#                 # toggle description on label
#                 elif desc and react_bootstrap:
#                     collapse = (
#                         '<Collapse in="OPEN"><div id="'
#                         + f"Vocab-{rty_ID}"
#                         + '" >'
#                         + desc
#                         + "</div></Collapse>"
#                     )
#                     li.append(etree.fromstring(collapse))

#             return td

#     def format_reference_url(self):
#         if not self.dty_SemanticReferenceURL:
#             return etree.fromstring("<td/>")
#         else:
#             a = f'<a class="link" target="_blank" rel="noreferrer noopener" href="{self.dty_SemanticReferenceURL}">{self.dty_SemanticReferenceURL}</a>'
#             return etree.fromstring(f"<td>{a}</td>")

#     def format_requirement_type(self):
#         s = '<span class="badge badge-{}">{}</span>'
#         name = self.rst_RequirementType.capitalize()
#         if self.rst_RequirementType == "required":
#             badge = "success"
#         elif self.rst_RequirementType == "recommended":
#             badge = "primary"
#         elif self.rst_RequirementType == "optional":
#             badge = "secondary"
#         elif self.rst_RequirementType == "forbidden":
#             badge = "dark"
#             name = "Outmoded"
#         return etree.fromstring(f"<td>{s.format(badge, name)}</td>")

#     def format_target_record_types(
#         self, present_records: list, record_name_index: dict
#     ):
#         if not self.dty_PtrTargetRectypeIDs:
#             return etree.fromstring("<td/>")
#         if self.dty_PtrTargetRectypeIDs:
#             l = []
#             for i in sorted([int(x) for x in self.dty_PtrTargetRectypeIDs.split("|")]):
#                 name = record_name_index[i]
#                 if i in present_records:
#                     l.append(f'<a class="link" href="#{i}">{name}</a>')
#                 else:
#                     l.append(name)
#             s = f'<td>{", ".join(l)}</td>'
#             return etree.fromstring(s)

#     def format_data_type(self):
#         name = self.dty_Type.capitalize()
#         if self.dty_Type == "enum":
#             name = "Vocabulary"
#         elif self.dty_Type == "freetext" or self.dty_Type == "blocktext":
#             name = "Text"
#         elif self.dty_Type == "resource":
#             name = "Foreign key"
#         return etree.fromstring(f"<td>{name}</td>")

#     def format_help_text(self):
#         return build_element_with_text("td", self.dty_HelpText)

#     def transform_non_section_fields(
#         self,
#         present_records: list,
#         record_name_index: dict,
#         react_bootstrap: bool,
#         rty_ID: int,
#     ) -> list[etree.Element]:
#         return [
#             etree.fromstring(f"<td>{self.rst_DisplayName}</td>"),
#             etree.fromstring(f"<td>{self.rst_DetailTypeID}</td>"),
#             self.format_help_text(),
#             self.format_reference_url(),
#             self.format_requirement_type(),
#             self.format_data_type(),
#             self.format_target_record_types(
#                 present_records=present_records, record_name_index=record_name_index
#             ),
#             self.format_vocab_terms(react_bootstrap=react_bootstrap, rty_ID=rty_ID),
#         ]

#     def build_tr(self):
#         tr = etree.Element("tr", **{"class": "table-light"})
#         return tr

#     def convert_n_row(
#         self,
#         record_name_index: dict,
#         present_records: list,
#         react_bootstrap: bool,
#         rty_ID: int,
#     ) -> etree.Element:
#         tr = self.build_tr()
#         for td in self.transform_non_section_fields(
#             present_records=present_records,
#             record_name_index=record_name_index,
#             react_bootstrap=react_bootstrap,
#             rty_ID=rty_ID,
#         ):
#             tr.append(td)
#         return tr

#     def convert_to_first_row(
#         self,
#         rowspan: int,
#         record_name_index: dict,
#         present_records: list,
#         react_bootstrap: bool,
#         rty_ID: int,
#     ) -> etree.Element:
#         tr = self.build_tr()
#         sec = f'<th scope="row" rowspan="{rowspan}">{self.sec}</th>'
#         sec = etree.fromstring(sec)
#         tr.append(sec)

#         for td in self.transform_non_section_fields(
#             present_records=present_records,
#             record_name_index=record_name_index,
#             react_bootstrap=react_bootstrap,
#             rty_ID=rty_ID,
#         ):
#             tr.append(td)

#         return tr
