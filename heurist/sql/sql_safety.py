import re

import duckdb

KEYWORDS = duckdb.sql("select * from duckdb_keywords()").fetchall()


class SafeSQLName:
    def __init__(self) -> None:
        self.reserved = [t[0] for t in KEYWORDS if t[1] == "reserved"]
        self.unreserved = [t[0] for t in KEYWORDS if t[1] == "unreserved"]
        self.column_name = [t[0] for t in KEYWORDS if t[1] == "column_name"]
        self.type_function = [t[0] for t in KEYWORDS if t[1] == "type_function"]
        self.all_keywords = [t[0] for t in KEYWORDS]

    @classmethod
    def remove_characters(cls, s: str) -> str:
        """Simplify and remove undesirable characters from a string.

        Examples:
        >>> s = "Author or Creator (Person, Organization)"
        >>> SafeSQLName.remove_characters(s)
        'Author or Creator'

        >>> s = "Status_trad_freetext"
        >>> SafeSQLName.remove_characters(s)
        'Status_trad_freetext'

        Args:
            s (str): Input string.

        Returns:
            str: Cleaned string.
        """

        # Remove parentheses
        s = re.sub(r"\(.+\)", "", s)
        # Remove non-letters
        s = re.sub(r"\W", " ", s)
        # Remove backslashes
        s = re.sub(r"/", " ", s)
        # Remove double spaces
        s = re.sub(r"\s+", " ", s)
        # Remove double underscores
        s = re.sub(r"_+", "_", s)
        # Trim underscores
        s = s.strip()
        return s

    @classmethod
    def to_pascal_case(cls, text: str) -> str:
        text_string = text.replace("-", " ").replace("_", " ")
        words = text_string.split()
        if len(text) == 0:
            return text
        capitalized_words = ["".join(w[0].capitalize() + w[1:] for w in words)]
        return "".join(capitalized_words)

    def create_column_name(self, field_name: str, field_type: str) -> str:
        """
        Create an SQL-safe column name for the Pydantic data field.

        Args:
            field_name (str): Displayed name of the field (detail) in Heurist.
            field_type (str): Heurist type of the field (detail).

        Returns:
            str: SQL-safe column name.
        """

        simplified_name = self.remove_characters(field_name)
        if field_type == "resource":
            final_name = f"{simplified_name} H-ID"
        elif simplified_name.lower() in self.all_keywords:
            final_name = f"{simplified_name}_COLUMN"
        else:
            final_name = simplified_name
        return final_name

    def create_table_name(self, record_name: str) -> str:
        """
        Create SQL-safe table name for the record's data model.

        Examples:
        >>> heurist_name = "Sequence"
        >>> SafeSQLName().create_table_name(heurist_name)
        'SequenceTable'

        Args:
            record_name (str): Name of the Heurist record type.

        Returns:
            str: SQL-safe name for the record type's table.
        """

        camel_case_name = self.to_pascal_case(record_name)
        if camel_case_name.lower() in self.all_keywords:
            final_name = f"{camel_case_name}Table"
        else:
            final_name = camel_case_name
        return final_name
