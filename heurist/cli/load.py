"""
CLI command for extracting, transforming, and loading remote Heurist data.
"""

from pathlib import Path

import duckdb

from heurist.api.client import HeuristAPIClient
from heurist.workflows import extract_transform_load


def load_command(
    client: HeuristAPIClient,
    duckdb_database_connection_path: Path | str,
    record_group: tuple,
    user: tuple,
    outdir: Path,
    require_compound_dates: bool = False,
):
    # Run the ETL process
    with duckdb.connect(duckdb_database_connection_path) as conn:
        extract_transform_load(
            client=client,
            duckdb_connection=conn,
            record_group_names=record_group,
            user=user,
            require_compound_dates=require_compound_dates,
        )

    # Show the results of the created DuckDB database
    with duckdb.connect(duckdb_database_connection_path) as new_conn:
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
