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
        "value": {
            "start": {
                "earliest": "1180",
                "latest": "1231",
                "profile": "1",  # central
            },
            "end": {
                "latest": "1250",
                "earliest": "1246",
                "profile": "3",  # slowFinish
            },
            "determination": "2",  # conjecture
            "estMinDate": 1180,
            "estMaxDate": 1250.1231,
        },
        "fieldName": "date_of_creation",
        "fieldType": "date",
        "conceptID": "",
    },
    {
        "dty_ID": 1111,
        "value": {
            "start": {"earliest": "1454"},
            "end": {"latest": "1456"},
            "estMinDate": 1454,
            "estMaxDate": 1456.1231,
        },
        "fieldName": "date_of_creation",
        "fieldType": "date",
        "conceptID": "",
    },
]

# Result of src.heurist_transformers.prepare_records.RecordFlattener
PYDANTIC_KEY_VALUE = {
    "DTY1111": [
        [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31, 0, 0)],
        [datetime(1454, 1, 1, 0, 0), datetime(1456, 12, 31, 0, 0)],
    ],
    "DTY1111_TEMPORAL": [
        {
            "start": {
                "earliest": datetime(1180, 1, 1, 0, 0),  # "1180"
                "latest": datetime(1231, 1, 1, 0, 0),  # "1231"
                "estProfile": "central",  # 1
                "estDetermination": None,
            },
            "end": {
                "latest": datetime(1250, 1, 1, 0, 0),  # "1250"
                "earliest": datetime(1246, 1, 1, 0, 0),  # "1246"
                "estProfile": "slowFinish",  # 3
                "estDetermination": None,
            },
            "estDetermination": "conjecture",  # 2
            "estProfile": None,
            "estMinDate": datetime(1180, 1, 1, 0, 0),  # 1180
            "estMaxDate": datetime(1250, 12, 31, 0, 0),  # 1250.1231
            "timestamp": None,
        },
        {
            "start": {
                "earliest": datetime(1454, 1, 1, 0, 0),
                "latest": None,
                "estProfile": None,
                "estDetermination": None,
            },
            "end": {
                "earliest": None,
                "latest": datetime(1456, 1, 1, 0, 0),
                "estProfile": None,
                "estDetermination": None,
            },
            "estMinDate": datetime(1454, 1, 1, 0, 0),  # 1454
            "estMaxDate": datetime(1456, 12, 31, 0, 0),  # 1456.1231
            "estDetermination": None,
            "estProfile": None,
            "timestamp": None,
        },
    ],
}

# Result of validating flattened data in the record's DynamicRecordTypeModel
ALIAS_KEY_VALUE = {
    "date_of_creation": [
        [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31, 0, 0)],
        [datetime(1454, 1, 1, 0, 0), datetime(1456, 12, 31, 0, 0)],
    ],
    "date_of_creation_TEMPORAL": [
        {
            "start": {"earliest": "1180", "latest": "1231", "estProfile": "1"},
            "end": {"latest": "1250", "earliest": "1246", "estProfile": "3"},
            "estDetermination": "2",
            "estMinDate": 1180,
            "estMaxDate": 1250.1231,
        },
        {
            "start": {"earliest": "1454"},
            "end": {"latest": "1456"},
            "estMinDate": 1454,
            "estMaxDate": 1456.1231,
        },
    ],
}
