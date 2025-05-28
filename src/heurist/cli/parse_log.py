import csv
from pathlib import Path

import click
from heurist.log import LogDetail, yield_log_blocks
from heurist.log.constants import VALIDATION_LOG

log_detail_fieldnames = list(LogDetail.__annotations__.keys())


@click.command()
@click.option("-l", "--log-file", required=None, default=VALIDATION_LOG)
@click.option("-o", "--outfile", required=None, default="invalid_records.csv")
def cli(log_file, outfile):
    logfile = Path(log_file)
    if not logfile.is_file():
        raise FileNotFoundError(log_file)
    with open(logfile) as f, open(outfile, "w") as of:
        writer = csv.DictWriter(of, fieldnames=log_detail_fieldnames)
        writer.writeheader()
        lines = f.readlines()
        for block in yield_log_blocks(lines):
            writer.writerow(block.__dict__)


if __name__ == "__main__":
    cli()
