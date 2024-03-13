import click
from heurist_api.client import HeuristAPIClient
from heurist_api.parsers.db_structure import DBStructure
from heurist_api.parsers.record import RecordParser
from pathlib import Path


@click.command("dump")
@click.option("-d", "--db", type=click.STRING, help="Name of the database")
@click.option("-s", "--sessionid", type=click.STRING, help="Session ID cookie")
@click.option(
    "-r", "--record", "records", type=(click.INT, click.STRING), multiple=True
)
@click.option("-o", "--outdir", type=click.Path(file_okay=False, dir_okay=True))
def cli(db, sessionid, records, outdir):
    outdir = Path(outdir)
    if not outdir.is_dir():
        outdir.mkdir()

    client = HeuristAPIClient(db=db, session_id=sessionid)

    fp = client.export_structure(output=outdir)

    parser = DBStructure(db_xml=fp)

    for record_id, record_name in records:
        table = parser.build_table(rst_ID=record_id, name=record_name)

        fp = client.export_records(record_type_id=record_id, output=outdir)

        record_parser = RecordParser(record_xml=fp, table=table, output=outdir)

        record_parser.convert()


if __name__ == "__main__":
    cli(obj={})
