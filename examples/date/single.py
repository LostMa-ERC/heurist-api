from dataclasses import dataclass

DETAIL_FUZZY = {
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

DETAIL_SIMPLE = {
    "dty_ID": 1111,
    "value": "2024-03-19",
    "fieldName": "date / time",
    "fieldType": "date",
    "conceptID": "",
}


@dataclass
class FuzzyDateProfile:
    flat = "0"
    central = "1"
    slowStart = "2"
    slowFinish = "3"


@dataclass
class FuzzyDateDetermination:
    unknown = "0"
    attested = "1"
    conjecture = "2"
    measurement = "3"
