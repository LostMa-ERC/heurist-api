from pathlib import Path


NS = {"hml": "https://heuristnetwork.org"}


HEURIST_SERVER = "https://heurist.huma-num.fr/heurist"


API_EXPORT = f"{HEURIST_SERVER}/export/xml/flathml.php"
EXPORT = (
    API_EXPORT + "?q=t%%3A%s&a=1&db=%s&depth=all&linkmode=direct"
)  # %(record_type_id, database_name)


API_DB_STRUCTURE = f"{HEURIST_SERVER}/hserv/structure/export/getDBStructureAsXML.php"
DB_STRUCTURE = API_DB_STRUCTURE + "?db=%s&ll=H6Default"  # %(database_name)
