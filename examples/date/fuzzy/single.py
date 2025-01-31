from datetime import datetime

# Result of joining the database schema tables
METADATA = {
    "dty_ID": 1111,
    "rst_DisplayName": "date_of_creation",
    "dty_Type": "date",
    "rst_MaxValues": 1,
}

# Result of a record's JSON export
DETAIL = {
    "dty_ID": 1111,
    "value": {
        "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        "end": {"latest": "1250", "earliest": "1246", "profile": "3"},
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
    "fieldName": "date / time",
    "fieldType": "date",
    "conceptID": "",
}


# Result of src.heurist_transformers.prepare_records.RecordFlattener
PYDANTIC_KEY_VALUE = {
    "DTY1111": [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31, 0, 0)],
    "DTY1111_TEMPORAL": {
        "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        "end": {"latest": "1250", "earliest": "1246", "profile": "3"},
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
}

# Result of validating flattened data in the record's DynamicRecordTypeModel
ALIAS_KEY_VALUE = {
    "date_of_creation": [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31, 0, 0)],
    "date_of_creation_TEMPORAL": {
        "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        "end": {"latest": "1250", "earliest": "1246", "profile": "3"},
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
}
