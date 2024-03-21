import json
import csv
from pathlib import Path
from typing import Dict, List, Generator
import logging
from pydantic import ValidationError

from heurist_api.schemas.dynamic_record import RecordBaseModel


logger = logging.getLogger(__name__)
logging.basicConfig(filename="warnings.log", level=logging.WARN)


class Records:
    model: RecordBaseModel
    root: List[RecordBaseModel]

    def __init__(self, model: RecordBaseModel) -> None:
        self.model = model
        self.root = []

    def validate_data(self, data: List[Dict]):
        for record in data:
            try:
                modeled_data = self.model(**record)
                if not isinstance(modeled_data, self.model):
                    raise TypeError
            except ValidationError as e:
                logger.warn(msg=e)
            else:
                self.root.append(modeled_data)

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
                writer.writerow(rowdict=row)
