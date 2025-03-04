import importlib.metadata

import click

from heurist.api.connection import HeuristConnection
from heurist.cli.load import load_command
from heurist.cli.records import rty_command
from heurist.cli.schema import schema_command
from heurist.utils.constants import DEFAULT_RECORD_GROUPS

__identifier__ = importlib.metadata.version("heurist")


# =========================== #
#     Main cli group
# =========================== #
@click.group(help="Group CLI command for connecting to the Heurist DB")
@click.version_option(__identifier__)
@click.option(
    "-d",
    "--database",
    type=click.STRING,
    help="Name of the Heurist database",
)
@click.option(
    "-l",
    "--login",
    type=click.STRING,
    help="Login name for the database user",
)
@click.option(
    "-p",
    "--password",
    type=click.STRING,
    help="Password for the database user",
)
@click.option(
    "--debugging",
    required=False,
    default=False,
    is_flag=True,
    help="Whether to run in debug mode, default false.",
)
@click.pass_context
def cli(ctx, database, login, password, debugging):
    ctx.ensure_object(dict)
    ctx.obj["DEBUGGING"] = debugging
    ctx.obj["CLIENT"] = HeuristConnection(
        database_name=database,
        login=login,
        password=password,
    )


# =========================== #
#     'record' command
# =========================== #
@cli.command("record", help="Get a JSON export of a certain record type.")
@click.option(
    "-t",
    "--record-type",
    help="The ID fo the record type",
    type=click.INT,
    required=True,
)
@click.option(
    "-o",
    "--outfile",
    help="JSON file path.",
    type=click.Path(file_okay=True, writable=True),
    required=False,
)
@click.pass_obj
def records(ctx, record_type, outfile):
    client = ctx["CLIENT"]
    rty_command(client, record_type, outfile)


# =========================== #
#     'schema' command
# =========================== #
@cli.command(
    "schema",
    help="Generate documentation about the database schema.",
)
@click.option(
    "-t",
    "--output-type",
    required=True,
    type=click.Choice(["csv", "json"], case_sensitive=False),
    help="Data format in which the schema will be described. \
    csv = 1 CSV file for each record type. json = 1 file that \
    lists all records together",
)
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
    show_default=True,
    help="Group name of the record types to be described. \
        Can be declared multiple times for multiple groups.",
)
@click.option(
    "-o",
    "--outdir",
    required=False,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Path to the directory in which the files will be written. \
        Defaults to name of the database + '_schema'.",
)
@click.pass_obj
def doc(ctx, record_group, outdir, output_type):
    # Get context variables
    client = ctx["CLIENT"]
    debugging = ctx["DEBUGGING"]

    # Run the doc command
    schema_command(
        client=client,
        record_group=record_group,
        outdir=outdir,
        output_type=output_type,
        debugging=debugging,
    )


# =========================== #
#     'download' command
# =========================== #
@cli.command(
    "download",
    help="Export data of records of 1 or more record group types.",
)
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=DEFAULT_RECORD_GROUPS,
    help="Record group of the entities whose data is exported. \
        Default: 'My record types'.",
)
@click.option(
    "-u",
    "--user",
    required=False,
    type=click.INT,
    multiple=True,
    help="User or users who created the records to be exported. \
        Default: all users' records.",
)
@click.option(
    "-f",
    "--filepath",
    required=True,
    type=click.Path(
        file_okay=True,
        dir_okay=False,
    ),
    help="Path to the DuckDB database file in which the data will be written.",
)
@click.option(
    "-o",
    "--outdir",
    required=False,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
    ),
    help="Directory in which CSV files of the dumped tabular data \
        will be written.",
)
@click.option(
    "--require-compound-dates",
    required=False,
    default=False,
    is_flag=True,
    show_default=True,
    help="Impose strict data validation on Heurist dates, requiring compound dates.",
)
@click.pass_obj
def load(ctx, filepath, record_group, user, outdir, require_compound_dates):
    # Get context variable
    client = ctx["CLIENT"]
    testing = ctx["DEBUGGING"]

    # Run the dump command
    if not testing:
        load_command(
            client=client,
            duckdb_database_connection_path=filepath,
            record_group=record_group,
            user=user,
            outdir=outdir,
            require_compound_dates=require_compound_dates,
        )
    else:
        print(
            "\nCannot run 'dump' command in debugging mode.\
            \nClient must connect to a remote Heurist database.\n"
        )
        print("Exiting.")
        exit()


if __name__ == "__main__":
    cli()
