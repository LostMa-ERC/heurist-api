"""
CLI command for downloading all requested record types' data.
"""

from pathlib import Path

import duckdb
from heurist.api.connection import HeuristAPIConnection
from heurist.api.credentials import CredentialHandler
from heurist.log import log_summary
from heurist.log.constants import VALIDATION_LOG
from heurist.utils.constants import DEFAULT_RECORD_GROUPS
from heurist.workflows import extract_transform_load
from rich.columns import Columns
from rich.console import Console, Group
from rich.padding import Padding
from rich.panel import Panel


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
        tables = [t[0] for t in new_conn.sql("show tables;").fetchall()]
        with open(VALIDATION_LOG) as f:
            log = f.readlines()
        show_summary_in_console(tables=tables, log_lines=log)

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


def show_summary_in_console(tables: list[str], log_lines: list[str]):
    console = Console()
    t0 = Panel(
        Columns(tables, equal=True, expand=True),
        title="SQL Tables",
        subtitle="Saved in DuckDB database file.",
    )
    t1, t2 = log_summary(lines=log_lines)
    panel_group = Group(Padding(t0, 1), t1, Padding(t2, 1))
    console.print(panel_group)
