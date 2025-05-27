import click
import csv
from heurist.log import yield_log_blocks, LogDetail


log_detail_fieldnames = list(LogDetail.__annotations__.keys())


@click.command()
@click.argument("csvfile", type=click.Path())
@click.option("-l", "--log-file", required=None, default="validation.log")
def cli(csvfile, log_file):
    with open(log_file) as f, open(csvfile, "w") as of:
        writer = csv.DictWriter(of, fieldnames=log_detail_fieldnames)
        writer.writeheader()
        lines = f.readlines()
        for block in yield_log_blocks(lines):
            writer.writerow(block.__dict__)


if __name__ == "__main__":
    cli()
