"""Module for utilities commonly used by XML parsers in schemas."""

import json


def split_ids(input: str) -> list:
    """Function for converting a string representation of a list of quoted integers \
        into a Python list object.

    Examples:
        >>> s = "3001,3110,3113,3288"
        >>> split_ids(s)
        [3001, 3110, 3113, 3288]
        >>> s = '[\\"3001\\",\\"3110\\",\\"3113\\",\\"3288\\"]'
        >>> split_ids(s)
        [3001, 3110, 3113, 3288]
        >>> l = ['[\\"3001\\",\\"3110\\",\\"3113\\",\\"3288\\"]']
        >>> split_ids(l)
        [3001, 3110, 3113, 3288]
        >>> s = '[]'
        >>> split_ids(s)
        []

    Args:
        input (str|Any): List of integers.

    Returns:
        list: _description_
    """

    # Handle input of potentially malformatted JSON list
    if isinstance(input, list) or "[" in input:
        if not isinstance(input, str):
            s = json.dumps(input)
            if not isinstance(s, str):
                print(input)
                raise TypeError("Integer list was not converted to string.")
        else:
            s = input

        # Remove the JSON string escape characters
        s = s.replace("\\", "")
        s = s.replace('"', "")
        s = s.replace("[", "")
        s = s.replace("]", "")

        input_string = s

    else:
        input_string = input

    # Split and recast regular string
    return [int(i) for i in input_string.split(",") if i != ""]
