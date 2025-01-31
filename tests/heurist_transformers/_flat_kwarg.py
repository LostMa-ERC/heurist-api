from datetime import datetime

ONE_RESOURCE = {
    "DTY1244": "Aie d'Avignon",
    "DTY1246": "45",
}

TWO_RESOURCES = {
    "DTY1244": "Aie d'Avignon",
    "DTY1246": ["45", "15"],
}

ONE_TEMPORAL = {
    "DTY1244": "Aie d'Avignon",
    "DTY1111": [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31)],
    "DTY1111_TEMPORAL": {
        "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        "end": {"latest": "1250", "earliest": "1246", "profile": "3"},
        "determination": "2",
        "estMinDate": 1180,
        "estMaxDate": 1250.1231,
    },
}

TWO_TEMPORAL = {
    "DTY1244": "Aie d'Avignon",
    "DTY1111": [
        [datetime(1180, 1, 1, 0, 0), datetime(1250, 12, 31)],
        [datetime(1200, 1, 1, 0, 0), datetime(1240, 12, 31)],
    ],
    "DTY1111_TEMPORAL": [
        {
            "determination": "2",
            "end": {"earliest": "1246", "latest": "1250", "profile": "3"},
            "estMaxDate": 1250.1231,
            "estMinDate": 1180,
            "start": {"earliest": "1180", "latest": "1231", "profile": "1"},
        },
        {
            "determination": "2",
            "end": {"earliest": "1236", "latest": "1240", "profile": "3"},
            "estMaxDate": 1240.1231,
            "estMinDate": 1200,
            "start": {"earliest": "1200", "latest": "1210", "profile": "1"},
        },
    ],
}

ONE_ENUM = {
    "DTY1244": "Aie d'Avignon",
    "DTY1107": "Disease",
    "DTY1107_TRM": "5391",
}

TWO_ENUM = {
    "DTY1244": "Aie d'Avignon",
    "DTY1107": ["Disease", "Disease.Epidemic.Spanish Flu"],
    "DTY1107_TRM": ["5391", "6535"],
}
