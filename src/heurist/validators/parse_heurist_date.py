import re
from heurist.models.dynamic import HistoricalDate

FLOAT_RE = re.compile(r"^(-?\d+)\.(\d{2}|\d{4})$")
ISO_RE = re.compile(r"^(-?\d+)(?:-(\d{1,2})(?:-(\d{1,2}))?)?$")

def parse_heurist_date(h_date: str | int | float | None) -> HistoricalDate | None:
    """
    Convert Heurist's partial date representations to an ISO-compatible format.

    Examples:
        >>> # Test a string representation of a date
        >>> v = "2024-03-19"
        >>> parse_heurist_date(v)
        HistoricalDate(year=2024, month=3, day=19, iso='2024-03-19')

        >>> # Test an integer representation of a year, i.e. circa 1188
        >>> v = 1188
        >>> parse_heurist_date(v)
        HistoricalDate(year=1188, month=None, day=None, iso='1188-01-01')

        >>> # Test a float representation of a date
        >>> v = 1250.1231
        >>> parse_heurist_date(v)
        HistoricalDate(year=1250, month=12, day=31, iso='1250-12-31')

    Args:
        h_date (str | int | float): Heurist representation \
            of a date.

    Returns:
        HistoricalDate | None: Parsed date.
    """

    if h_date is None:
        return None

    # Affirm Heurist's representation of the date is a Python string
    h_date = str(h_date).strip()

    m = FLOAT_RE.match(h_date)
    if m:
        year = int(m.group(1))
        rest = m.group(2)

        if len(rest) == 2:
            month = int(rest)
            day = None
        elif len(rest) == 4:
            month = int(rest[:2])
            day = int(rest[2:])
        else:
            raise ValueError(f"Invalid date: {h_date}")

    else:
        m = ISO_RE.match(h_date)
        if not m:
            raise ValueError(f"Invalid date: {h_date}")

        year = int(m.group(1))
        month = int(m.group(2)) if m.group(2) is not None else None
        day = int(m.group(3)) if m.group(3) is not None else None

    return HistoricalDate(
        year=year,
        month=month,
        day=day
    )
