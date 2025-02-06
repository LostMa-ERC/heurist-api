import click

from src.api_client import HeuristClient
from src.cli_commands import doc_command, dump_command, rty_command

from .__version__ import __identifier__


# =========================== #
#     Main cli group
# =========================== #
@click.group(help="Group CLI command for connecting to the Heurist OLTP DB")
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
    "--testing",
    required=False,
    default=False,
    is_flag=True,
    help="Whether to run in debug mode, default false.",
)
@click.pass_context
def cli(ctx, database, login, password, testing):
    ctx.ensure_object(dict)
    ctx.obj["TESTING"] = testing
    ctx.obj["CLIENT"] = HeuristClient(
        database_name=database, login=login, password=password, testing=testing
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
    help="Command to export documentation \
             about the database schema.",
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
    testing = ctx["TESTING"]

    # Run the doc command
    doc_command(client, testing, record_group, outdir, output_type)


# =========================== #
#     'dump' command
# =========================== #
@cli.command(
    "dump",
    help="Command to export data of records of a given \
        record group type.",
)
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
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
def dump(ctx, filepath, record_group, user: tuple[int], outdir):
    # Get context variable
    client = ctx["CLIENT"]
    testing = ctx["TESTING"]

    # Run the dump command
    if not testing:
        dump_command(client, filepath, record_group, user, outdir)
    else:
        print(
            "\nCannot run 'dump' command in debugging mode.\
            \nClient must connect to a remote Heurist database.\n"
        )
        print("Exiting.")
        exit()


if __name__ == "__main__":
    cli()
