"""Module for utilities commonly used by XML parsers in schemas."""

import re


def split_ids(input: str | None) -> str | None:
    """Function for converting a string representation of a list of quoted integers into a Python list object.

    Examples:
        >>> s = "3001,3110,3113,3288"
        >>> split_ids(s)
        '3001|3110|3113|3288'

    Args:
        input (str|Any): String representation of a list.

    Returns:
        list: _description_
    """
    ids = []
    if isinstance(input, str):
        # if "[" in input:
        #     s = re.sub(r"\\\"", "", input)
        #     s = re.sub("[\[|\]]", "", s)
        #     s = re.sub(r"\\\&quot;", "", s)
        #     s = s.split(",")
        #     for i in s:
        #         if i == "":
        #             i = None
        #         ids.append(i)
        # else:
        ids = [i.strip() for i in input.split(",") if i]
    if len(ids) > 0:
        return "|".join(ids)
