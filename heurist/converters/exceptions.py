"""
   Exceptions for classes that convert / transform Heurist data.
"""


class RepeatedValueInSingularDetailType(Exception):
    """The detail type is limited to a maximum of 1 values
    but the record has more than 1 value for this detail."""

    description = """The detail '{}' is limited to a maximum of 1 values.\
\n\tCount of values = {}"""

    def __init__(self, detail_name: str, value_count: int):
        self.message = self.description.format(detail_name, value_count)
        super().__init__(self.message)


class DateNotEnteredAsDateObject(Exception):
    """The date field was not entered as a constructed Heurist date object."""

    description = """The date field was not entered as a compound Heurist date \
object.\n\tEntered value = {}"""

    def __init__(self, value: int | str | float):
        self.message = self.description.format(value)
        super().__init__(self.message)
