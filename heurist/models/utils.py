"""Module for utilities commonly used by XML parsers in schemas."""

import re
from typing import Any


def split_ids(input: str | Any) -> list[int]:
    """Function for converting a string representation of a list of quoted integers into a Python list object.

    Examples:
        >>> s = r'[\&quot;3001\&quot;,\&quot;3110\&quot;,\&quot;3113\&quot;,\&quot;3288\&quot;]'
        >>> split_ids(s)
        [3001, 3110, 3113, 3288]

    Args:
        input (str|Any): String representation of a list.

    Returns:
        list: _description_
    """

    f = []
    if isinstance(input, str):
        s = re.sub(r"\\\"", "", input)
        s = re.sub("[\[|\]]", "", s)
        s = re.sub(r"\\\&quot;", "", s)
        s = s.split(",")
        for i in s:
            if i == "":
                i = None
            else:
                i = int(i)
            f.append(i)
    return f
