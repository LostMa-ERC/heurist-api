"""
CLI command for downloading details about a Heurist database schema.
"""

from pathlib import Path

from heurist.api.connection import HeuristAPIConnection
from heurist.api.credentials import CredentialHandler
from heurist.database import TransformedDatabase
from heurist.schema import output_csv, output_json
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def get_database_schema(
    record_groups: list,
    credentials: CredentialHandler,
    debugging: bool,
) -> TransformedDatabase:
    # If testing, load the mock database XML schema
    if debugging:
        from mock_data import DB_STRUCTURE_XML

        db = TransformedDatabase(
            hml_xml=DB_STRUCTURE_XML, record_type_groups=record_groups
        )
    # If not testing, request the database XML schema from the server
    else:
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
            _ = p.add_task("Downloading schemas")
            xml = client.get_structure()
            db = TransformedDatabase(
                hml_xml=xml,
                record_type_groups=record_groups,
            )
    return db


def schema_command(
    credentials: CredentialHandler,
    record_group: list,
    outdir: str,
    output_type: str,
    debugging: bool = False,
):
    # Set up the output directory
    if not outdir:
        outdir = f"{credentials.get_database()}_schema"
    DIR = Path(outdir)
    DIR.mkdir(exist_ok=True)

    # Get the database schema
    db = get_database_schema(
        record_groups=record_group,
        credentials=credentials,
        debugging=debugging,
    )

    # Describe each targeted record type
    record_type_ids = list(db.pydantic_models.keys())
    with Progress(
        TextColumn("{task.description}"), BarColumn(), MofNCompleteColumn()
    ) as p:
        descriptions = []
        t = p.add_task("Describing record types", total=len(record_type_ids))
        for id in record_type_ids:
            rel = db.describe_record_schema(rty_ID=id)
            descriptions.append(rel)
            p.advance(t)

    # Output the descriptions according to the desired data format
    if output_type == "csv":
        output_csv(dir=DIR, descriptions=descriptions)

    elif output_type == "json":
        outfile = DIR.joinpath("recordTypes.json")
        output_json(descriptions=descriptions, fp=outfile)
