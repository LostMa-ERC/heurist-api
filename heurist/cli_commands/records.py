"""CLI command for extracting, transforming, and loading remote Heurist data."""

import json
from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from heurist.src.api_client import HeuristClient


def rty_command(client: HeuristClient, rty: int, outfile: Path | str | None):
    with Progress(
        TextColumn("{task.description}"),
        SpinnerColumn(),
        TimeElapsedColumn(),
    ) as p:
        _ = p.add_task(f"Get Records of type {rty}", total=1)
        records = client.get_records(rty)
    if not outfile:
        outfile = f"RTY_{rty}.json"
    if not isinstance(outfile, Path):
        outfile = Path(outfile)
    print(f"Writing results to: {outfile}")
    with open(outfile, "w") as f:
        json.dump(records, f, indent=4)
