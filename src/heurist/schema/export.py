from pathlib import Path
import json
from datetime import date
import duckdb

from heurist.api.connection import HeuristAPIConnection
from heurist.database import TransformedDatabase
from heurist.schema.rel_to_dict import convert_rty_description
from heurist.sql.sql_safety import SafeSQLName
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

def output_csv(dp: Path, descriptions: list[duckdb.DuckDBPyRelation]) -> None:
    for rel in descriptions:
        name = rel.select("rty_Name").limit(1).fetchone()[0]
        safe_name = SafeSQLName().create_table_name(name)
        fp = dp.joinpath(safe_name).with_suffix(".csv")
        rel.write_csv(file_name=str(fp), header=True)


def output_json(descriptions: list[duckdb.DuckDBPyRelation], fp: Path) -> None:
    date_string = date.today().isoformat()
    data = {"lastModified": date_string, "items": []}
    for desc in descriptions:
        kv_dict = convert_rty_description(description=desc)
        for id, metadata in kv_dict.items():
            d = {"id": id} | metadata
            data["items"].append(d)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_database_schema(
    record_groups: list,
    db_name:str,
    login: str,
    password: str,
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
                db=db_name,
                login=login,
                password=password,
            ) as client,
        ):
            _ = p.add_task("Downloading schemas")
            xml = client.get_structure()
            db = TransformedDatabase(
                hml_xml=xml,
                record_type_groups=record_groups,
            )
    return db


def export_schema(
    db_name:str,
    login: str,
    password: str,
    record_group: list,
    outdir: str,
    output_type: str,
    debugging: bool = False,
):
    # Set up the output directory
    if not outdir:
        outdir = f"{db_name}_schema"
    DIR = Path(outdir)
    DIR.mkdir(exist_ok=True)

    # Get the database schema
    db = get_database_schema(
        record_groups=record_group,
        db_name=db_name,
        login=login,
        password=password,
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
        output_csv(dp=DIR, descriptions=descriptions)

    elif output_type == "json":
        outfile = DIR.joinpath("recordTypes.json")
        output_json(descriptions=descriptions, fp=outfile)
