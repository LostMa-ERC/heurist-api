from typing import Any
import lxml.html
from lxml import etree


def escape_escape_characters(s: Any) -> str | None:
    if s:
        s = str(s)
        s = s.replace(r"\"", '"')
        s = s.replace(r"\'", "'")
        s = s.replace(r"\n", "\n")
        s = s.replace("<br>", "<br/>")
        return s


def build_element_with_text(
    tag: str, text: str, cls: str | None = None, attrs: dict | None = None
) -> etree.Element:
    text = escape_escape_characters(text)
    attributes = ""
    if cls or attrs:
        if cls:
            attributes += f' class="{cls}"'
        elif attrs:
            for k, v in attrs.items():
                attributes += f' {k}="{v}"'
    s = f"<{tag}{attributes}>{text}</{tag}>"
    return lxml.html.fromstring(s)