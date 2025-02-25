from datetime import datetime

import dateutil
import dateutil.parser
import dateutil.relativedelta

from heurist import setup_logger, DATABASE_LOG

logger = setup_logger(name="validate-pydantic-model", filepath=DATABASE_LOG)


class HeuristDateHandler:

    @classmethod
    def list_min_max(
        cls, date_representations: str | int | float | list[str | str | float]
    ) -> list[datetime]:
        """
        Convert Heurist's representation of dates into a list of Python datetime \
            objects, representing the earliest and latest dates in the given values.

        Examples:
            >>> # Test a string representation of a date
            >>> v = "2024-03-19"
            >>> HeuristDateHandler.list_min_max(v)
            [datetime.datetime(2024, 3, 19, 0, 0), None]

            >>> # Test an integer representation of a year, i.e. circa 1188
            >>> v = 1188
            >>> HeuristDateHandler.list_min_max(v)
            [datetime.datetime(1188, 1, 1, 0, 0), None]

            >>> # Test a list of date representations
            >>> v = [1180, 1250.1231]
            >>> HeuristDateHandler.list_min_max(v)
            [datetime.datetime(1180, 1, 1, 0, 0), datetime.datetime(1250, 12, 31, 0, 0)]

        Args:
            date_representations (str | int | float | list[str | int | float]): \
                Heurist's representation of dates.

        Returns:
            list[datetime]: Ordered list of the earliest and latest dates.
        """

        if isinstance(date_representations, list):
            d1, d2 = cls.parse(date_representations[0]), cls.parse(
                date_representations[1]
            )
            date_list = sorted([d1, d2])
        else:
            date_representations = str(date_representations)
            date_list = [cls.parse(date_representations), None]
        return date_list

    @classmethod
    def fill_out_date_str(cls, date_representation: str | int | float) -> str:
        """
        Convert Heurist's partial date representations to an ISO string format.

        Examples:
            >>> # Test a string representation of a date
            >>> v = "2024-03-19"
            >>> HeuristDateHandler.fill_out_date_str(v)
            '2024-03-19'

            >>> # Test an integer representation of a year, i.e. circa 1188
            >>> v = 1188
            >>> HeuristDateHandler.fill_out_date_str(v)
            '1188-01-01'

            >>> # Test a float representation of a date
            >>> v = 1250.1231
            >>> HeuristDateHandler.fill_out_date_str(v)
            '1250-12-31'

        Args:
            date_representation (str | int | float): Heurist representation of a date.

        Returns:
            str: ISO string format of a date, YYYY-MM-DD.
        """

        # Affirm the representation is a string
        s = str(date_representation)

        # If the Heurist representation is a year, change it to the start of the year.
        if len(s) == 4:
            return f"{s}-01-01"

        # If the Heurist representation is a float, parse the month and day
        # shown after the decimal.
        elif "." in s:
            splits = s.split(".")
            year, smaller_than_year = splits[0], splits[1]
            if len(smaller_than_year) == 2:
                return f"{year}-{smaller_than_year}-01"
            elif len(smaller_than_year) == 4:
                return f"{year}-{smaller_than_year[:2]}-{smaller_than_year[2:]}"

        # If the Heurist representation is a year and month, add the day
        # (first of the month)
        parts = s.split("-")
        if len(parts) == 2:
            return f"{s}-01"

        # If no other conditions have been met, the representation is already in
        # ISO format YYYY-MM-DD.
        else:
            return s

    @classmethod
    def parse(cls, date_representation: str | int | float) -> datetime:
        """
        Parse a single date's representation into a Python datetime object.

        Args:
            date_representation (str | int | float): Heurist date representation.

        Returns:
            datetime: Datetime object representing a date in Heurist data.
        """

        v = cls.fill_out_date_str(date_representation)
        try:
            return dateutil.parser.parse(v)
        except Exception as e:
            logger.warning(e)
