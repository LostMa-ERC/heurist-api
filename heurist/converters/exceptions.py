"""
   Exceptions for classes that convert / transform Heurist data.
"""


class RepeatedValueInSingularDetailType(Exception):
    """The detail type is limited to a maximum of 1 values
    but the record has more than 1 value for this detail."""

    description = """The detail type is limited to a maximum of 1 values, \
but {} values were found."""

    def __init__(self, detail_type_id: int, value_count: int):
        self.message = f"DTY: {detail_type_id}\t{self.description.format(value_count)}"
        super().__init__(self.message)


class DateNotEnteredAsDateObject(Exception):
    """The date field was not entered as a constructed Heurist date object."""

    description = (
        """The date field was not entered as a constructed Heurist date object."""
    )

    def __init__(self, detail_type_id: int):
        self.message = f"DTY: {detail_type_id}\t{self.description}"
        super().__init__(self.message)
