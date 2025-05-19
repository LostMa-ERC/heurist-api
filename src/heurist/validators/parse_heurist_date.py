from datetime import datetime

import dateutil.parser
import dateutil.relativedelta


def parse_heurist_date(repr: str | int | float | None) -> datetime | None:
    """
    Convert Heurist's partial date representations to an ISO string format.

    Examples:
        >>> # Test a string representation of a date
        >>> v = "2024-03-19"
        >>> parse_heurist_date(v)
        datetime.datetime(2024, 3, 19, 0, 0)

        >>> # Test an integer representation of a year, i.e. circa 1188
        >>> v = 1188
        >>> parse_heurist_date(v)
        datetime.datetime(1188, 1, 1, 0, 0)

        >>> # Test a float representation of a date
        >>> v = 1250.1231
        >>> parse_heurist_date(v)
        datetime.datetime(1250, 12, 31, 0, 0)

    Args:
        repr (str | int | float): Heurist representation \
            of a date.

    Returns:
        datetime | None: Parsed date.
    """

    if not repr:
        return

    # Affirm Heurist's representation of the date is a Python string
    repr = str(repr)

    # If the Heurist representation is a year, change it to the start of
    # the year.
    if len(repr) == 4:
        iso_str = f"{repr}-01-01"
        return dateutil.parser.parse(iso_str)

    # If the Heurist representation is a float, parse the month and day
    # shown after the decimal.
    elif "." in repr:
        splits = repr.split(".")
        year, smaller_than_year = splits[0], splits[1]
        if len(smaller_than_year) == 2:
            iso_str = f"{year}-{smaller_than_year}-01"
        elif len(smaller_than_year) == 4:
            iso_str = f"{year}-{smaller_than_year[:2]}-{smaller_than_year[2:]}"
        else:
            raise ValueError(repr)
        return dateutil.parser.parse(iso_str)

    # If the Heurist representation is a year and month, add the day
    # (first of the month)
    parts = repr.split("-")
    if len(parts) == 2:
        iso_str = f"{repr}-01"
        return dateutil.parser.parser(iso_str)

    # If no other conditions have been met, the representation is already in
    # ISO format YYYY-MM-DD.
    else:
        iso_str = repr
        return dateutil.parser.parse(iso_str)
