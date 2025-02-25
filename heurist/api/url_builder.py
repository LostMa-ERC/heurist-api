"""Class to compose URIs for calling the Heurist API."""

from typing import Literal

from heurist.api.constants import (
    HUMA_NUM_SERVER,
    RECORD_JSON_EXPORT_PATH,
    RECORD_XML_EXPORT_PATH,
    STRUCTURE_EXPORT_PATH,
)

COMMA = "%2C"
COLON = "%3A"


class URLBuilder:
    """Class to construct endpoints for the Heurist API (on Huma-Num's server)."""

    def __init__(self, database_name: str, server: str = HUMA_NUM_SERVER) -> None:
        self.server = server
        self.database_name = database_name

    @property
    def db_api(self) -> str:
        return f"{self.server}{STRUCTURE_EXPORT_PATH}"

    @property
    def xml_record_api(self) -> str:
        return f"{self.server}{RECORD_XML_EXPORT_PATH}"

    @property
    def json_record_api(self) -> str:
        return f"{self.server}{RECORD_JSON_EXPORT_PATH}"

    @classmethod
    def _join_queries(cls, *args) -> str:
        """Join 1 or more queries together with an ampersand.

        Returns:
            str: Fragment of a path for the URL.
        """
        return "&".join([a for a in args if a is not None])

    @classmethod
    def _join_list_items(cls, *args) -> str:
        """Join 1 or more items in a list of queries.

        Examples:
            >>> item1 = '{"filter"%3A"value"}'
            >>> item2 = '{"filter"%3A"value"}'
            >>> item3 = '{"filter"%3A"value"}'
            >>> URLBuilder._join_list_items(item1, item2, item3)
            '[{"filter"%3A"value"}%2C{"filter"%3A"value"}%2C{"filter"%3A"value"}]'

        Returns:
            str: Fragment of a path for the URL.
        """
        start = "["
        end = "]"
        items = COMMA.join([a for a in args if a is not None])
        return f"{start}{items}{end}"

    @classmethod
    def _make_filter_obj(cls, filter: str, value: str | int) -> str:
        start = "{"
        end = "}"
        return f'{start}"{filter}"{COLON}"{value}"{end}'

    @classmethod
    def _join_comma_separated_values(cls, *args) -> str:
        return COMMA.join([str(a) for a in args if a is not None])

    def get_db_structure(self) -> str:
        """
        URL to retrieve the database structure.

        Examples:
            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.get_db_structure()
            'https://heurist.huma-num.fr/heurist/hserv/structure/export/getDBStructureAsXML.php?db=mock_db'

        Returns:
            str: URL to retrieve the database structure.
        """
        db = f"?db={self.database_name}"
        return f"{self.db_api}{db}"

    def get_records(
        self,
        record_type_id: int,
        form: Literal["xml", "json"] = "xml",
        users: tuple = (),
    ) -> str:
        """Build a URL to retrieve records of a certain type.

        Examples:
            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.get_records(101)
            'https://heurist.huma-num.fr/heurist/export/xml/flathml.php?q=[{"t"%3A"101"}%2C{"sortby"%3A"t"}]&a=1&db=mock_db&depth=all&linkmode=direct_links'

            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.get_records(102, form="json")
            'https://heurist.huma-num.fr/heurist/hserv/controller/record_output.php?q=[{"t"%3A"102"}%2C{"sortby"%3A"t"}]&a=1&db=mock_db&depth=all&linkmode=direct_links&format=json&defs=0&extended=2'

            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.get_records(102, users=(2,16,))
            'https://heurist.huma-num.fr/heurist/export/xml/flathml.php?q=[{"t"%3A"102"}%2C{"sortby"%3A"t"}%2C{"addedby"%3A"2%2C16"}]&a=1&db=mock_db&depth=all&linkmode=direct_links'


        Args:
            record_type_id (int): Heurist ID of the record type.
            form (Literal["xml", "json"]): The format of the exported data.

        Returns:
            str: URL to retrieve records of a certain type.
        """

        a = "a=1"
        db = "db=%s" % (self.database_name)
        depth = "depth=all"
        link_mode = "linkmode=direct_links"

        if form == "json":
            api = self.json_record_api
            format_args = "format=json&defs=0&extended=2"
        else:
            api = self.xml_record_api
            format_args = None

        # Make the query based on parameters
        record_type_filter = self._make_filter_obj(filter="t", value=record_type_id)
        sortby_filter = self._make_filter_obj(filter="sortby", value="t")
        if len(users) > 0:
            user_string = self._join_comma_separated_values(*users)
            users_filter = self._make_filter_obj(filter="addedby", value=user_string)
        else:
            users_filter = None
        query_path = self._join_list_items(
            record_type_filter, sortby_filter, users_filter
        )
        query = f"?q={query_path}"

        path = self._join_queries(query, a, db, depth, link_mode, format_args)
        return f"{api}{path}"
