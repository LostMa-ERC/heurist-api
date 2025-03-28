# Download record groups

## Require date fields to have metadata

```shell
heurist download -f NEW_DATABASE.db --require-compound-dates
```

Heurist offers a rich way of registering compound date information, including date ranges, uncertain dates, as well as details about a fuzzy date's certainty and probability distribution. However, Heurist also allows users to directly type a date estimate, i.e. a year (`1448`), in the record's field.

If you want to confirm that all your records' dates have compound dates, with comparable metadata, use the `heurist download` command with the `--require-compound-dates` flag. This flag imposes an extra step of data validation that causes records without compound dates to be reported in the `validation.log` file (see the [Log section](./logs.md)) and not included in the DuckDB database produced at the end of the workflow.

### Example of an invalid date field in the log

A user can enter a year directly in a date field, without going through Heurist's compound date widget or, as in the case of CSV import, indicating a date range. When using the `--require-compound-dates` flag, this record would fail validation and be reported in the log.

```txt
2025-02-27 12:19:03,378 validation  WARNING
    Record: text    Record ID: 47644
    DTY: 1285   The date field was not entered as a compound Heurist date object.
    Entered value = 1448
```

If you want to impose this strict date data validation for your analysis, go back to Heurist and change the reported record's date.

## Understanding Heurist date metadata

### How Heurist's API describes dates

To better understand how the `heurist` ETL package processes Heurist date data, look at how Heurist's API transmits the data stored in the database.

#### Simple date detail

Simple date detail from Heurist's API:

```json
{
    "dty_ID": 1285,
    "value": 1448,
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": ""
}
```

The value of a simple date detail from Heurist's API is a year or date string (i.e. `1448`). If the `--require-compound-dates` flag is used in the `heurist download` command, a simple date detail will raise a warning and cause the record to be invalid.

#### Compound date detail

Compound date detail from Heurist's API:

```json
{
    "dty_ID": 1285,
    "value": {
        "start": {
            "earliest": "1460"
        },
        "end": {
            "latest": "1469"
        },
        "estMinDate": 1460,
        "estMaxDate": 1469.1231
    },
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": ""
},
```

The value of a compound date detail from Heurist's API is a map of metadata, including the data's earliest (`estMinDate`) and latest (`estMaxDate`) dates.

### How the `heurist` package processes compound dates

For every 1 date field, the `heurist` ETL process creates 2 columns, which aim to (i) transform the data into an efficient format and (ii) preserve the original information returned from Heurist's API.

#### Input examples from Heurist API

Let's look at an example with a date field named `date_of_creation` and 3 records.

**Record 1: `date_of_creation` _1180 - 1200_**

```json
{
    "start": {
        "earliest": "1180"
    },
    "end": {
        "latest": "1200"
    },
    "estMinDate": 1180,
    "estMaxDate": 1200.1231
}
```

**Record 2: `date_of_creation` _in 1448_** (implied, simple date)

```json
{
    "dty_ID": 1285,
    "value": 1448,
    "fieldName": "date_of_creation",
    "fieldType": "date",
    "conceptID": ""
}
```

**Record 3: `date_of_creation` _circa 1188_**

```json
{
    "timestamp": {
        "in": "1188",
        "type": "s",
        "circa": true
    },
    "comment": "1188",
    "estMinDate": 1188,
    "estMaxDate": 1188
}
```

#### Date column

The estimated minimum and maximum dates are extracted from Heurist's compound date metadata, transformed into Python `datetime` objects, arranged in an ordered list of the earliest and latest dates in the data field.

|Record|Compound|Meaning|`estMinDate` from API|`estMinDate` from API|created `date_of_creation` column|
|--|--|--|--|--|--|
|1|yes|1180 - 1200|`1180`|`1200.1231`|`[1180-01-01 00:00:00, 1200-12-31 00:00:00]`|
|2|no|in 1448|||`[1448-01-01 00:00:00, NULL]`|
|3|yes|circa 1188|`1188`|`1188`|`[1188-01-01 00:00:00, 1188-01-01 00:00:00]`|

#### Map column

In addition to the parsed `date_of_creation` column, the `heurist` ETL pipeline also preserves the response from Heurist's API in a supplemental column with the suffix `_TEMPORAL` if it is of a compound date.

|Record|created `date_of_creation` column|created `date_of_creation_TEMPORAL` column|
|--|--|--|
|1|`[1180-01-01 00:00:00, 1200-12-31 00:00:00]`|`{'start': {'earliest': '1180'}, 'end': {'latest': '1200'}, 'estMinDate': 1180, 'estMaxDate': 1200.1231}`|
|2|`[1448-01-01 00:00:00, NULL]`||
|3|`[1188-01-01 00:00:00, 1188-01-01 00:00:00]`|`{'timestamp': {'in': '1188', 'type': 's', 'circa': True}, 'comment': '1188', 'estMinDate': 1188, 'estMaxDate': 1188}`|
