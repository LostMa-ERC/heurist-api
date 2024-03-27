import json
from pathlib import Path
import logging
from pydantic import ValidationError
from typing import Generator

from heurist_api.schemas import RelationshipMarker
from heurist_api.client import HeuristAPIClient
from heurist_api.utils import load_json

logger = logging.getLogger(__name__)


class RelationshipMarkers:
    model = RelationshipMarker

    def __init__(self, client: HeuristAPIClient) -> None:
        json_load = load_json(client=client, record_id=1)
        data = json_load.get("heurist", {}).get("records")
        self.root = []
        for record in data:
            try:
                # Validate the data in the model
                modeled_data = self.model(**record)
                self.root.append(modeled_data)
            except ValidationError as e:
                logger.warn(msg=e)

    def __iter__(self) -> Generator[RelationshipMarker | None, None, None]:
        yield from self.root

    def to_json_strings(self) -> list:
        return [json.loads(m.model_dump_json()) for m in self.root]

    def to_delimited_json(self, outfile: Path):
        with open(outfile, "w") as f:
            for s in self.to_json_strings():
                l = f"{json.dumps(s, ensure_ascii=False)}\n"
                f.write(l)
