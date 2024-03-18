from heurist_api.constants import (
    HEURIST_SERVER,
    RECORD_JSON_EXPORT_PATH,
    RECORD_XML_EXPORT_PATH,
    STRUCTURE_EXPORT_PATH,
)


class URLBuilder:
    """
    Constructor of endpoints for the Heurist API.
    """

    server = HEURIST_SERVER
    xml_record_api = HEURIST_SERVER + RECORD_XML_EXPORT_PATH
    json_record_api = HEURIST_SERVER + RECORD_JSON_EXPORT_PATH
    db_api = HEURIST_SERVER + STRUCTURE_EXPORT_PATH

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def join_parts(self, *args) -> str:
        return "&".join([a for a in args if a is not None])

    def record(self, record_type_id: str | int, format: str = "xml") -> str:
        """Build a URL to retrieve records of a certain type.

        Examples:
            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.record(101)
            'https://heurist.huma-num.fr/heurist/export/xml/flathml.php?q=[{"t"%3A"101"}%2C{"sortby"%3A"t"}]&a=1&db=mock_db&depth=all&linkmode=direct'

            >>> db = "jbcamps_gestes"
            >>> builder = URLBuilder(db)
            >>> builder.record(102, format="json")
            'https://heurist.huma-num.fr/heurist/hserv/controller/record_output.php?q=t%3A102&a=1&db=jbcamps_gestes&depth=all&linkmode=direct&format=json&defs=0&extended=2'

        Args:
            record_type_id (str | int): Heurist ID of the record type.

        Returns:
            str: URL to retrieve records of a certain type.
        """

        a = "a=1"
        api = self.xml_record_api
        db = "db=%s" % (self.database_name)
        depth = "depth=all"
        link_mode = "linkmode=direct"

        if format == "json":
            api = self.json_record_api
            query = "?q=t%%3A%s" % (record_type_id)
            format_args = "format=json&defs=0&extended=2"
        else:
            api = self.xml_record_api
            query = '?q=[{"t"%%3A"%s"}%%2C{"sortby"%%3A"t"}]' % (record_type_id)
            format_args = None

        return api + self.join_parts(query, a, db, depth, link_mode, format_args)

    @property
    def structure(self) -> str:
        """
        URL to retrieve the database structure.

        Examples:
            >>> db = "mock_db"
            >>> builder = URLBuilder(db)
            >>> builder.structure
            'https://heurist.huma-num.fr/heurist/hserv/structure/export/getDBStructureAsXML.php?db=mock_db&ll=H6Default'

        Returns:
            str: URL to retrieve the database structure.
        """
        db = "?db=%s" % (self.database_name)
        version = "ll=H6Default"
        return self.db_api + self.join_parts(db, version)
