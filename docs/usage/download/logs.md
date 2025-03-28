# Download record groups

## Logs

All uses of the `heurist download` command generate a log file that helps you assess your data's validity in the Heurist database.

This log reports every record in the Heurist database whose data does not match the schema you've designed for the record type in Heurist.

- Heurist allows users to save records that are invalid.
- The `heurist download` command requires that records' data is valid according to the schema declared in the Heurist database's architecture.
- Any records that violate the schema are not loaded into the local DuckDB database, and they are reported in the `validation.log` file.
- It is advised that you go back to your Heurist database and fix the invalid records.

### Example log report of invalid Heurist record

For example, if you have designed the data field of a Heurist record to allow only 1 value, but it has been saved with multiple, an error will be logged in `validation.log`.

```txt
2025-03-28 17:12 - WARNING -
    [rec_Type 104]
    [rec_ID 834]
    The detail 'note' is limited to a maximum of 1 values.
    Count of values = 3.
```

In this example, we see the problematic record has the ID `837` and is a `stemma` record. The problematic detail is `note` and it was saved with 3 values, while it should be limited to 1. In Heurist, we should either correct the record or modify the schema, then re-run the `heurist download` command. Invalid records are not loaded in the DuckDB database.

## Name changes

To adapt the names of record types and data fields to PL/SQL syntax and DuckDB, sometimes changes are made.

### Reserved names & keywords

When a table or column name is a [reserved term](https://en.wikipedia.org/wiki/List_of_SQL_reserved_words) or keyword in DuckDB's SQL dialect, a suffix is appended.

- Heurist record named `Sequence` &rarr; Table named `SequenceTable`
- Heurist data field named `language` &rarr; Column named `language_COLUMN`

To see a current list of DuckDB's reserved keywords, connect to a DuckDB database instance and execute the command  `select * from duckdb_keywords();`.

### Foreign keys / Heurist pointer

A Heurist record's data field can point to another Heurist record, which Heurist refers to as a "resource" or "pointer."

To make the CSV files that you can generate with `heurist download` useful for updating your Heurist database, we append `H-ID` to the end of every referential column, as required for Heurist import.

- Heurist pointer field named `is_part_of` -> Column named `is_part_of H-ID`

### Vocabulary terms

When a Heurist record's data field points to a vocabulary term, the `heurist` package generates columns for both the term's label and a unique identifier (foreign key) referring to a term in the `trm` table.

- Heurist vocabulary field named `country`

    1. &rarr; Column named `country` (term's label)
    2. &rarr; Column named `country TRM-ID` (term's ID, refers to `trm` table)

### Heurist dates

When a Heurist record's data field is a date, the `heurist` package generates 2 columns. See a full discusion on [How the `heurist` package processes compound dates](./date_validation.md#how-the-heurist-package-processes-compound-dates).
