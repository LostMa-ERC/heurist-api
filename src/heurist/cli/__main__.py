"""
CLI commands for extracting, transforming, and loading remote Heurist data.
"""

import importlib.metadata

import click
from heurist import PACKAGE_NAME
from heurist.api.credentials import CredentialHandler
from heurist.api.exceptions import MissingParameterException
from heurist.cli.load import load_command
from heurist.cli.records import rty_command
from heurist.cli.schema import schema_command
from heurist.utils.constants import DEFAULT_RECORD_GROUPS
from rich.console import Console

# This name must match the package name ('name' kwarg) in the TOML file.
__identifier__ = importlib.metadata.version(PACKAGE_NAME)


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
    try:
        ctx.obj["CREDENTIALS"] = CredentialHandler(
            database_name=database,
            login=login,
            password=password,
        )
    except MissingParameterException:
        c = Console()
        c.print(
            "Login informaiton is missing."
            "Please provide your credentials when prompted."
            "\nTo quit, press Ctrl+C then Enter."
        )
        _database = click.prompt("Heurist database name")
        _login = click.prompt("Heurist user login")
        _password = click.prompt("Heurist login password")
        c.print("Retrying the connection...")
        ctx.obj["CREDENTIALS"] = CredentialHandler(
            database_name=_database,
            login=_login,
            password=_password,
        )
        c.print("Success!", style="green")


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
    credentials = ctx["CREDENTIALS"]
    rty_command(credentials, record_type, outfile)


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
    credentials = ctx["CREDENTIALS"]
    debugging = ctx["DEBUGGING"]

    # Run the doc command
    schema_command(
        credentials=credentials,
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
@click.pass_obj
def load(ctx, filepath, record_group, user, outdir):
    # Get context variable
    credentials = ctx["CREDENTIALS"]
    testing = ctx["DEBUGGING"]

    # Run the dump command
    if not testing:
        load_command(
            credentials=credentials,
            duckdb_database_connection_path=filepath,
            record_group=record_group,
            user=user,
            outdir=outdir,
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
