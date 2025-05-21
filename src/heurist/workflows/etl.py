import duckdb
from heurist.api.connection import HeuristAPIConnection
from heurist.database import TransformedDatabase
from heurist.utils.constants import DEFAULT_RECORD_GROUPS
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


def extract_transform_load(
    client: HeuristAPIConnection,
    duckdb_connection: duckdb.DuckDBPyConnection,
    user: tuple = (),
    record_group_names: tuple = DEFAULT_RECORD_GROUPS,
) -> None:
    """
    Workflow for (1) extracting, transforming, and loading the Heurist database \
        architecture into a DuckDB database and (2) extracting, transforming, \
        and loading record types' records into the created DuckDB database.

    Args:
        client (HeuristAPIConnection): Context of a Heurist API connection.
        duckdb_connection (duckdb.DuckDBPyConnection): Connection to a DuckDB database.
        user (tuple): IDs (integers) of targeted users.
        record_group_names (tuple): Names of the record group types. Must include at \
            least 1. Defaults to ("My record types").

    Returns:
        duckdb.DuckDBPyConnection: Open connection to the created DuckDB database.
    """

    # Export the Heurist database's structure
    with Progress(
        TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
    ) as p:
        _ = p.add_task("Get DB Structure")
        xml = client.get_structure()

    # Export individual record sets and insert into the DuckDB database
    with (
        Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        ) as p,
    ):
        database = TransformedDatabase(
            conn=duckdb_connection,
            hml_xml=xml,
            record_type_groups=record_group_names,
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
