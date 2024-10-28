from typing import Any
import lxml.html
from lxml import etree


def escape_escape_characters(s: Any) -> str | None | dict:
    if isinstance(s, str) or isinstance(s, int):
        s = str(s)
        s = s.replace(r"\"", '"')
        s = s.replace(r"\'", "'")
        s = s.replace(r"\n", "\n")
        s = s.replace("<br>", "<br/>")
        return s
    else:
        return s


def build_element_with_text(
    tag: str, text: str, cls: str | None = None, attrs: dict | None = None
) -> etree.Element:
    if not text:
        raise ValueError("Must have text")
    text = escape_escape_characters(text)
    text = text.replace('target="_blank"', 'target="_blank" rel="noreferrer noopener"')
    attributes = ""
    if cls or attrs:
        if cls:
            attributes += f' class="{cls}"'
        elif attrs:
            for k, v in attrs.items():
                attributes += f' {k}="{v}"'
    s = f"<{tag}{attributes}>{text}</{tag}>"
    return lxml.html.fromstring(s)
