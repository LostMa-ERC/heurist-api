"""
CLI command for extracting, transforming, and loading remote Heurist data.
"""

from pathlib import Path

import duckdb
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


def load_command(
    client: HeuristAPIClient,
    filepath: Path,
    record_group: tuple,
    user: tuple,
    outdir: Path,
    require_date_object: bool = False,
):
    # Export the Heurist database's structure
    with Progress(
        TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
    ) as p:
        _ = p.add_task("Get DB Structure")
        xml = client.get_structure()

    # Export individual record sets and insert into the DuckDB database
    with (
        duckdb.connect(filepath) as conn,
        Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        ) as p,
    ):
        database = TransformedDatabase(
            conn=conn,
            hml_xml=xml,
            record_type_groups=record_group,
            require_date_object=require_date_object,
        )
        t = p.add_task(
            "Get Records",
            total=len(database.pydantic_models.keys()),
        )
        for record_type in database.pydantic_models.values():
            rty_ID = record_type.rty_ID
            records = client.get_records(rty_ID, users=user)
            p.advance(t)
            database.insert_records(record_type_id=rty_ID, records=records)

    # Show results of DuckDB database
    with duckdb.connect(filepath) as new_conn:
        tables = new_conn.sql("show tables;")
        print("\nCreated the following tables")
        print(tables)
        if outdir:
            outdir = Path(outdir)
            outdir.mkdir(exist_ok=True)
            for tup in tables.fetchall():
                table_name = tup[0]
                # Skip the schema tables
                if table_name in ["rtg", "rst", "rty", "dty", "trm"]:
                    continue
                fp = outdir.joinpath(f"{table_name}.csv")
                new_conn.table(table_name).sort("H-ID").write_csv(str(fp))
