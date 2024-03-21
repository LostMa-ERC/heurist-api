import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Generator
import logging
from pydantic import ValidationError

from heurist_api.schemas.dynamic_record import RecordBaseModel


logger = logging.getLogger(__name__)
logging.basicConfig(filename="warnings.log", level=logging.WARN, filemode="w")


class Records:
    model: RecordBaseModel
    root: List[RecordBaseModel]

    def __init__(self, model: RecordBaseModel) -> None:
        self.model = model
        self.root = []

    def validate_data(self, data: List[Dict]):
        for record in data:
            try:
                # Validate the data in the model
                modeled_data = self.model(**record)
                self.root.append(modeled_data)
            except ValidationError as e:
                logger.warn(msg=e)

    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self) -> Generator[RecordBaseModel | None, None, None]:
        yield from self.root

    def to_delimited_json(self, outfile: Path):
        json_strings = [json.loads(m.model_dump_json()) for m in self.root]
        with open(outfile, "w") as f:
            for s in json_strings:
                l = f"{json.dumps(s, ensure_ascii=False)}\n"
                f.write(l)

    @property
    def serialized_model_fieldnames(self) -> List:
        fieldnames = []
        for annotation in self.model.model_fields.values():
            key = annotation.default.__metadata__[0].serialization_alias
            fieldnames.append(key)
        return fieldnames

    def to_csv(self, outfile: Path):
        headers = list(self.serialized_model_fieldnames)
        with open(outfile, "w") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for record in self.root:
                row = record.model_dump()
                csv_safe_row = self.make_row_csv_safe(row)
                writer.writerow(rowdict=csv_safe_row)

    @classmethod
    def make_row_csv_safe(cls, row: Dict):
        return {k: cls.concat_list(v) for k, v in row.items()}

    @classmethod
    def concat_list(cls, v: Any, separator: str = "|"):
        if isinstance(v, List):
            if len(v) == 1:
                v = f"{v[0]}"
            else:
                v = separator.join(f"{d}" for d in v)
        return v
