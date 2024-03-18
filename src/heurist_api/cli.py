import click
from pathlib import Path

from heurist_api.client import HeuristAPIClient


@click.command("dump")
@click.option("-d", "--db", type=click.STRING, help="Name of the database")
@click.option("-s", "--sessionid", type=click.STRING, help="Session ID cookie")
@click.option(
    "-r", "--record", "records", type=(click.INT, click.STRING), multiple=True
)
@click.option("-o", "--outdir", type=click.Path(file_okay=False, dir_okay=True))
def cli(db, sessionid, records, outdir):
    pass


if __name__ == "__main__":
    cli(obj={})
