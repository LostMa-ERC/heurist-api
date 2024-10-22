from pathlib import Path

import click
import duckdb
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from heurist.client import HeuristClient
from heurist.components.database.database import Database
from heurist.components.sql_models.sql_safety import SafeSQLName

from .__version__ import __identifier__


@click.group()
@click.version_option(__identifier__)
@click.option("-d", "--database", type=click.STRING)
@click.option("-l", "--login", type=click.STRING)
@click.option("-p", "--password", type=click.STRING)
@click.pass_context
def cli(ctx, database, login, password):
    ctx.obj = HeuristClient(database_name=database, login=login, password=password)


@cli.command("doc")
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
)
@click.option(
    "-o", "--outdir", required=True, type=click.Path(file_okay=False, dir_okay=True)
)
@click.pass_obj
def doc(client, record_group, outdir):
    DIR = Path(outdir)
    DIR.mkdir(exist_ok=True)
    namer = SafeSQLName()
    with Progress(
        TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
    ) as p:
        _ = p.add_task("Downloading architecture")
        xml = client.get_structure()
        db = Database(hml_xml=xml, record_type_groups=record_group)
        record_types = list(db.managers_record_type.keys())

    with Progress(
        TextColumn("{task.description}"), BarColumn(), MofNCompleteColumn()
    ) as p:
        t = p.add_task("Describing record types", total=len(record_types))
        for id in record_types:
            r = db.describe_record_fields(id)
            name = r.aggregate("rty_Name").fetchone()[0]
            safe_name = SafeSQLName().create_table_name(name)
            fp = DIR.joinpath(safe_name).with_suffix(".csv")
            r.write_csv(file_name=str(fp), header=True)
            p.advance(t)


@cli.command("dump")
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
)
@click.option(
    "-f", "--filepath", required=True, type=click.Path(file_okay=True, dir_okay=False)
)
@click.option(
    "-o", "--outdir", required=False, type=click.Path(file_okay=False, dir_okay=True)
)
@click.pass_obj
def dump(client, filepath, record_group, outdir):
    # Export the Heurist database's structure
    with Progress(
        TextColumn("{task.description}"), SpinnerColumn(), TimeElapsedColumn()
    ) as p:
        _ = p.add_task("Get DB Structure")
        xml = client.get_structure()

    # Export individual record sets and insert into the DuckDB database
    with duckdb.connect(filepath) as conn, Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as p:
        database = Database(conn=conn, hml_xml=xml, record_type_groups=record_group)
        t = p.add_task("Get Records", total=len(database.managers_record_type.keys()))
        for record_type in database.managers_record_type.values():
            rty_ID = record_type.rty_ID
            records = client.get_records(rty_ID)
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
                fp = outdir.joinpath(f"{table_name}.csv")
                new_conn.table(table_name).sort("H-ID").write_csv(str(fp))


if __name__ == "__main__":
    cli()
