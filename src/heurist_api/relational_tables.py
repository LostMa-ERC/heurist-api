import csv
from pathlib import Path

from heurist_api.record_parser import Records


class IDTypeRelations:
    def __init__(self) -> None:
        self.ids = []

    def append(self, records: Records) -> None:
        record_type = records.model.get_record_type()
        for json_string in records.to_json_strings():
            id = json_string.get("H-ID")
            assert id != None
            self.ids.append((id, record_type))

    def to_csv(self, outfile: Path) -> None:
        with open(outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["H-ID", "Recod Type"])
            writer.writerows(self.ids)
