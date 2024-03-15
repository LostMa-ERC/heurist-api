import re


NS = {"hml": "https://heuristnetwork.org"}

HEURIST_SERVER = "https://heurist.huma-num.fr/heurist"

API_EXPORT = f"{HEURIST_SERVER}/export/xml/flathml.php"
EXPORT = (
    API_EXPORT
    + '?q=[{"t"%%3A"%s"}%%2C{"sortby"%%3A"t"}]&a=1&db=%s&depth=all&linkmode=direct'
)  # %(record_type_id, database_name)

API_DB_STRUCTURE = f"{HEURIST_SERVER}/hserv/structure/export/getDBStructureAsXML.php"
DB_STRUCTURE = API_DB_STRUCTURE + "?db=%s&ll=H6Default"  # %(database_name)


class Query:
    def __init__(self, query_string: str) -> None:
        self.query_string = query_string

    @property
    def id(self):
        return re.search(r"(\d+)", self.query_string).group(0)
