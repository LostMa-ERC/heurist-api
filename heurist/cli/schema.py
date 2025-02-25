"""
CLI command for extracting, transforming, and loading details
about the Heurist database structure.
"""

from pathlib import Path

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from heurist.api.client import HeuristAPIClient
from heurist.database import TransformedDatabase
from heurist.schema import output_csv, output_json


def schema_command(
    client: HeuristAPIClient,
    testing: bool,
    record_group: tuple,
    outdir: str,
    output_type: str,
):
    # Set up the output directory
    if not outdir:
        outdir = f"{client.database_name}_schema"
    DIR = Path(outdir)
    DIR.mkdir(exist_ok=True)

    # Get the database's schemas
    if not testing:
        with Progress(
            TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
        ) as p:
            _ = p.add_task("Downloading schemas")
            xml = client.get_structure()
            db = TransformedDatabase(hml_xml=xml, record_type_groups=record_group)
            record_types = list(db.pydantic_models.keys())
    else:
        from heurist.mock_data import DB_STRUCTURE_XML

        db = TransformedDatabase(
            hml_xml=DB_STRUCTURE_XML, record_type_groups=record_group
        )
        record_types = list(db.pydantic_models.keys())

    # Describe each targeted record type
    with Progress(
        TextColumn("{task.description}"), BarColumn(), MofNCompleteColumn()
    ) as p:
        descriptions = []
        t = p.add_task("Describing record types", total=len(record_types))
        for id in record_types:
            descriptions.append(db.describe_record_schema(rty_ID=id))
            p.advance(t)

    # Output the descriptions according to the desired data format
    if output_type == "csv":
        output_csv(dir=DIR, descriptions=descriptions)

    elif output_type == "json":
        outfile = DIR.joinpath("recordTypes.json")
        output_json(descriptions=descriptions, fp=outfile)
