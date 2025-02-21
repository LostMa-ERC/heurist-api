# Result of joining the database schema tables
METADATA = {
    "dty_ID": 1114,
    "rst_DisplayName": "is_expression_of",
    "dty_Type": "resource",
    "rst_MaxValues": 0,
}

# Result of a record's JSON export
DETAIL = [
    {
        "dty_ID": 1114,
        "value": {
            "id": "36",
            "type": "103",
            "title": "Dagobert",
            "hhash": None,
        },
        "fieldName": "is_expression_of",
        "fieldType": "resource",
        "conceptID": "",
    },
    {
        "dty_ID": 1114,
        "value": {
            "id": "79",
            "type": "103",
            "title": "Garin le Lorrain",
            "hhash": None,
        },
        "fieldName": "is_expression_of",
        "fieldType": "resource",
        "conceptID": "",
    },
]

# Result of src.heurist_transformers.prepare_records.RecordFlattener
PYDANTIC_KEY_VALUE = {"DTY1114": [36, 79]}

# Result of validating flattened data in the record's DynamicRecordTypeModel
ALIAS_KEY_VALUE = {"is_expression_of H-ID": [36, 79]}
