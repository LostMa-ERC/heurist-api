from datetime import datetime

# Result of joining the database schema tables
METADATA = {
    "dty_ID": 1111,
    "rst_DisplayName": "date_of_creation",
    "dty_Type": "date",
    "rst_MaxValues": 0,
}

# Result of a record's JSON export
DETAIL = [
    {
        "dty_ID": 1111,
        "value": "2024-03-19",
        "fieldName": "date_of_creation",
        "fieldType": "date",
        "conceptID": "",
    },
    {
        "dty_ID": 1111,
        "value": {
            "timestamp": {"in": "1188", "type": "s", "circa": True},
            "comment": "1188",
            "estMinDate": 1188,
            "estMaxDate": 1188,
        },
        "fieldName": "date_of_creation",
        "fieldType": "date",
        "conceptID": "",
    },
]

# Detail's Pydantic field validation alias
# and the field's value for the Pydantic model
PYDANTIC_KEY_VALUE = {
    "DTY1111": [
        [datetime(2024, 3, 19, 0, 0), None],
        [datetime(1188, 1, 1, 0, 0), datetime(1188, 1, 1, 0, 0)],
    ],
    "DTY1111_TEMPORAL": [
        {
            "timestamp": {"in": "1188", "type": "s", "circa": True},
            "comment": "1188",
            "estMinDate": 1188,
            "estMaxDate": 1188,
        }
    ],
}

# Detail's serialization from the Pydantic field
ALIAS_KEY_VALUE = {
    "date_of_creation": [
        [datetime(2024, 3, 19, 0, 0), None],
        [datetime(1188, 1, 1, 0, 0), datetime(118, 12, 31, 0, 0)],
    ],
    "date_of_creation_TEMPORAL": [
        {
            "timestamp": {"in": "1188", "type": "s", "circa": True},
            "comment": "1188",
            "estMinDate": 1188,
            "estMaxDate": 1188,
        }
    ],
}
