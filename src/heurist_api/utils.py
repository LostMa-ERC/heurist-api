import json
from typing import Dict

from heurist_api.client import HeuristAPIClient


def load_json(client: HeuristAPIClient, record_id: int) -> Dict:
    json_bytes = client.get_records(record_type_id=record_id, form="json")
    json_string = json_bytes.decode("utf-8")
    json_load = json.loads(json_string)
    return json_load


# All records fed into an instance of the dynamic RecordModelBase
# must have the following keys, which are what Heurist exports:
mock_data = {
    "rec_RecTypeID": 100,  # ID of the record type (same for all records)
    "rec_ID": 1,  # ID of the individual record
    "details": [],  # Array of the record's details (fields)
}
