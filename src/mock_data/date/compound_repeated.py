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
