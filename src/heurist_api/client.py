import requests

from heurist_api.constants import EXPORT, DUMP_DIR, DB_STRUCTURE
from pathlib import Path


class HeuristAPIClient:
    """API Client for Heurist Database."""

    def __init__(self, db: str, session_id: str) -> None:
        """Initialize the API client.

        Parameters:
            db (str): Name of the database.
            session_id (str): Session ID cookie for authenticating user.
        """
        self.db = db
        self.session_id = session_id

    def export_records(self, record_type_id: int | str) -> Path:
        """Export all records of a given record type.

        Parameters:
            record_type_id (int|str): Heurist ID of the record type.

        Returns:
            fp (Path): A path to the HTML file containing the records.
        """
        url = EXPORT % (record_type_id, self.db)
        cookie = {"heurist-sessionid": self.session_id}

        r = requests.get(url=url, cookies=cookie)

        fp = DUMP_DIR.joinpath(f"records_{record_type_id}.html")

        with open(fp, "wb") as f:
            f.write(r.content)

        return fp

    def export_structure(self) -> Path:
        """Export the database's structure.

        Returns:
            fp (Path): A path to the HTML containing the database structure.
        """
        url = DB_STRUCTURE % (self.db)
        cookie = {"heurist-sessionid": self.session_id}

        r = requests.get(url=url, cookies=cookie)

        fp = DUMP_DIR.joinpath("db_structure.html")

        with open(fp, "wb") as f:
            f.write(r.content)

        return fp
