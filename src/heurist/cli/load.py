"""
CLI command for downloading all requested record types' data.
"""

from pathlib import Path

import duckdb
from heurist.api.connection import HeuristAPIConnection
from heurist.api.credentials import CredentialHandler
from heurist.utils.constants import DEFAULT_RECORD_GROUPS
from heurist.workflows import extract_transform_load


def load_command(
    credentials: CredentialHandler,
    duckdb_database_connection_path: Path | str,
    record_group: tuple = DEFAULT_RECORD_GROUPS,
    user: tuple = (),
    outdir: Path | None = None,
):
    # Run the ETL process
    if isinstance(duckdb_database_connection_path, Path):
        duckdb_database_connection_path = str(duckdb_database_connection_path)
    with (
        duckdb.connect(duckdb_database_connection_path) as conn,
        HeuristAPIConnection(
            db=credentials.get_database(),
            login=credentials.get_login(),
            password=credentials.get_password(),
        ) as client,
    ):
        extract_transform_load(
            client=client,
            duckdb_connection=conn,
            record_group_names=record_group,
            user=user,
        )

    # Show the results of the created DuckDB database
    with duckdb.connect(duckdb_database_connection_path) as new_conn:
        tables = new_conn.sql("show tables;")
        print("\nCreated the following tables")
        print(tables)

        # If writing to CSV files, write only tables of record types
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
