import click

from heurist.client import HeuristClient
from heurist.commands import doc_command, dump_command

from .__version__ import __identifier__


@click.group(help="Group CLI command for connecting to the Heurist OLTP DB")
@click.version_option(__identifier__)
@click.option(
    "-d", "--database", type=click.STRING, help="Name of the Heurist database"
)
@click.option(
    "-l", "--login", type=click.STRING, help="Login name for the database user"
)
@click.option(
    "-p", "--password", type=click.STRING, help="Password for the database user"
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


@cli.command("doc", help="Command to export documentation about the database schema.")
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
    # Get context variables
    client = ctx["CLIENT"]
    testing = ctx["TESTING"]

    # Run the doc command
    doc_command(client, testing, record_group, outdir, output_type)


@cli.command(
    "dump", help="Command to export data of records of a given record group type."
)
@click.option(
    "-r",
    "--record-group",
    required=False,
    type=click.STRING,
    multiple=True,
    default=["My record types"],
    help="Record group of the entities whose data is exported. Default: 'My record types'.",
)
@click.option(
    "-u",
    "--user",
    required=False,
    type=click.INT,
    multiple=True,
    help="User or users who created the records to be exported. Default: all users' records.",
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
    help="Directory in which CSV files of the dumped tabular data will be written.",
)
@click.pass_obj
def dump(ctx, filepath, record_group, user: tuple[int], outdir):
    # Get context variable
    client = ctx["CLIENT"]

    # Run the dump command
    dump_command(client, filepath, record_group, user, outdir)


if __name__ == "__main__":
    cli()
