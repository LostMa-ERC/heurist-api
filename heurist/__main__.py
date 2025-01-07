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
from heurist.doc import output_csv, output_json

from .__version__ import __identifier__


@click.group()
@click.version_option(__identifier__)
@click.option("-d", "--database", type=click.STRING)
@click.option("-l", "--login", type=click.STRING)
@click.option("-p", "--password", type=click.STRING)
@click.option("--testing", required=False, default=False, is_flag=True)
@click.pass_context
def cli(ctx, database, login, password, testing):
    ctx.ensure_object(dict)
    ctx.obj["TESTING"] = testing
    ctx.obj["CLIENT"] = HeuristClient(
        database_name=database, login=login, password=password, testing=testing
    )


@cli.command(
    "doc", help="Download and parse the schema of record types in the database."
)
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
    show_default=True,
    help="Group name of the record types to be described. Can be declared multiple times for multiple groups.",
)
@click.option(
    "-o",
    "--outdir",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Path to the directory in which the files will be written. Defaults to name of the database + '_schema'.",
)
@click.option(
    "-t",
    "--output-type",
    required=True,
    type=click.Choice(["csv", "json"], case_sensitive=False),
    help="Data format in which the schema will be described. csv = 1 CSV file for each record type. json = 1 file that lists all records together",
)
@click.pass_obj
def doc(ctx, record_group, outdir, output_type):
    client = ctx["CLIENT"]
    testing = ctx["TESTING"]
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
            db = Database(hml_xml=xml, record_type_groups=record_group)
            record_types = list(db.managers_record_type.keys())
    else:
        from examples import DB_STRUCTURE_XML

        db = Database(hml_xml=DB_STRUCTURE_XML, record_type_groups=record_group)
        record_types = list(db.managers_record_type.keys())

    # Describe each targeted record type
    with Progress(
        TextColumn("{task.description}"), BarColumn(), MofNCompleteColumn()
    ) as p:
        descriptions = []
        t = p.add_task("Describing record types", total=len(record_types))
        for id in record_types:
            descriptions.append(db.describe_record_fields(rty_ID=id))
            p.advance(t)

    # Output the descriptions according to the desired data format
    if output_type == "csv":
        output_csv(dir=DIR, descriptions=descriptions)

    elif output_type == "json":
        outfile = DIR.joinpath("recordTypes.json")
        output_json(descriptions=descriptions, fp=outfile)


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
    "-u",
    "--user",
    required=False,
    type=click.INT,
    multiple=True,
)
@click.option(
    "-f", "--filepath", required=True, type=click.Path(file_okay=True, dir_okay=False)
)
@click.option(
    "-o", "--outdir", required=False, type=click.Path(file_okay=False, dir_okay=True)
)
@click.pass_obj
def dump(ctx, filepath, record_group, user: tuple[int], outdir):
    client = ctx["CLIENT"]
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
                fp = outdir.joinpath(f"{table_name}.csv")
                new_conn.table(table_name).sort("H-ID").write_csv(str(fp))


if __name__ == "__main__":
    cli()
