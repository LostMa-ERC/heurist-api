# Main workflow for dumping records from Heurist database

from typing import List, Literal
from pathlib import Path
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    MofNCompleteColumn,
)

from heurist_api.client import make_client
from heurist_api.db_structure_parser import DBStructureParser
from heurist_api.record_parser import Records
from heurist_api.utils import load_json


def dump_records(
    database: str | None,
    login: str | None,
    password: str | None,
    record_ids: List[int],
    output: Path | str,
    form: Literal["json", "xml"],
):
    # Check output directory
    if not isinstance(output, Path):
        output = Path(output)
    if output.is_file():
        raise FileExistsError("Output needs to be a directory")
    output.mkdir(exist_ok=True)

    # Build a Heurist API client
    client = make_client(database_name=database, login=login, password=password)

    # Parse the Heurist database structure
    db_xml = client.get_structure()
    parser = DBStructureParser(xml=db_xml)

    # Dump each selected record type
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as p:
        task = p.add_task("Record Types", total=len(record_ids))

        for id in record_ids:
            # Design a model for the record type
            model = parser.create_record_model(record_type=id)
            records = Records(model=model)

            # Collect the record type's JSON export
            json_load = load_json(client=client, record_id=id)
            data = json_load.get("heurist", {}).get("records")

            n = len(data)
            print(f"{n} records found for record type {id}.")
            if n == 0:
                print(f"Skipping record type {id}.")
                p.advance(task)
                continue

            # Validate the export according to the model
            records.validate_data(data)

            # Write validated record results
            model_name = model.get_model_name()

            if form == "json":
                outfile = output.joinpath(f"{model_name}.json")
                records.to_delimited_json(outfile=outfile)

            elif form == "csv":
                outfile = output.joinpath(f"{model_name}.csv")
                records.to_csv(outfile=outfile)

                p.advance(task)
