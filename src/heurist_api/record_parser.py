import json
from pathlib import Path
from typing import Dict
import logging

from heurist_api.schemas.dynamic_record import RecordBaseModel
from heurist_api.db_structure_parser import DBStructureParser


logger = logging.getLogger(__name__)
logging.basicConfig(filename="warnings.log", level=logging.WARN)


class Records:
    def __init__(self, parser: DBStructureParser, record_type_id: int) -> None:
        self.model = parser.create_record_model(record_type=record_type_id)
        self.data = []

    def __call__(self, record: Dict):
        try:
            self.data.append(self.model(**record))
        except Exception as e:
            logger.warn(msg=e)

    def to_delimited_json(self, outfile: Path):
        json_strings = [json.loads(m.model_dump_json()) for m in self.data]
        with open(outfile, "w") as f:
            for s in json_strings:
                l = f"{json.dumps(s, ensure_ascii=False)}\n"
                f.write(l)
