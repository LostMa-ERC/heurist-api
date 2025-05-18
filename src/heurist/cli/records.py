"""
CLI command for downloading one requested record type's data.
"""

import json
from pathlib import Path

from heurist.api.connection import HeuristAPIConnection
from heurist.api.credentials import CredentialHandler
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def rty_command(
    credentials: CredentialHandler,
    rty: int,
    outfile: Path | str | None,
):
    with (
        Progress(
            TextColumn("{task.description}"),
            SpinnerColumn(),
            TimeElapsedColumn(),
        ) as p,
        HeuristAPIConnection(
            db=credentials.get_database(),
            login=credentials.get_login(),
            password=credentials.get_password(),
        ) as client,
    ):
        _ = p.add_task(f"Get Records of type {rty}", total=1)
        records = client.get_records(rty)
    # If no records of this type have been entered, stop.
    if len(records) == 0:
        print("No records of this type have been entered.\nExiting program...")
        exit()

    # Else, write the records to a JSON file.
    if not outfile:
        outfile = f"RTY_{rty}.json"
    if not isinstance(outfile, Path):
        outfile = Path(outfile)
    print(f"Writing results to: {outfile}")
    with open(outfile, "w") as f:
        json.dump(records, f, indent=4)
