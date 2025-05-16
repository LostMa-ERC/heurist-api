"""
Exceptions for classes that convert / transform Heurist data.
"""


class RepeatedValueInSingularDetailType(Exception):
    """The detail type is limited to a maximum of 1 values
    but the record has more than 1 value for this detail."""

    description = """
\t[rec_Type {typeID}]
\t[rec_ID {recID}]
\tThe detail '{fieldName}' is limited to a maximum of 1 values.
\tCount of values = {valueCount}."""

    def __init__(self, type_id: int, record_id: int, field_name: str, value_count: int):
        self.message = self.description.format(
            typeID=type_id,
            recID=record_id,
            fieldName=field_name,
            valueCount=value_count,
        )
        super().__init__(self.message)


class DateNotEnteredAsDateObject(Exception):
    """The date field was not entered as a constructed Heurist date object."""

    description = """The date field was not entered as a compound Heurist date \
object.\n\tEntered value = {}"""

    def __init__(self, value: int | str | float):
        self.message = self.description.format(value)
        super().__init__(self.message)
