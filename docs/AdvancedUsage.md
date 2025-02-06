# Advanced Usage

All use of the pipeline tool require access to a remote Heurist database. Therefore, before calling any of the commands, you will need to follow `heurist` with your login credentials and database name.

```shell
$ heurist -d DATBASE_NAME -l "USER.NAME" -p PASSWORD
```

## Dump

Use the `heurist dump` command to load your Heurist database's data into a local DuckDB database and/or export it in CSV files.

- [Basic Usage](#basic-usage)
- [CSV Export](#export-to-csv-files) : `--outdir` option
- [Filter on Record Type Group](#export-a-specific-record-type-group) : `--record-group` option
- [Filter on User](#export-a-specific-users-records) : `--user` option

```
Usage: heurist dump [OPTIONS]

  Command to export data of records of a given         record group type.

Options:
  -r, --record-group TEXT  Record group of the entities whose data is
                           exported.         Default: 'My record types'.
  -u, --user INTEGER       User or users who created the records to be
                           exported.         Default: all users' records.
  -f, --filepath FILE      Path to the DuckDB database file in which the data
                           will be written.  [required]
  -o, --outdir DIRECTORY   Directory in which CSV files of the dumped tabular
                           data         will be written.
  --help                   Show this message and exit.
```

### _Basic Usage_

To export your records from the Heurist database, saving them  in a DuckDB SQL database file, run the following:

```shell
$ heurist dump -f DATABASE.db
```

### _Export to CSV files_

To export your records to a DuckDB SQL database and save the tables as CSV files in a directory (`OUTDIR/`), run the following:

```shell
$ heurist dump -f DATABASE.db -o OUTDIR
```

### _Export a specific record type group_

When you don't declare a `--record-group`, the Heurist Data Pipeline Tool will automatically export all of the databse's records that are of the types declared in the group "My record types."

To export (and save in a DB file) records from your record types and another group, run the following:

```shell
$ heurist dump --record-group "My record types" --record-group "Bibliography" -f DATABASE.db
```

### _Export a specific user's records_

When you don't declare a specific `--user`, the Heurist Data Pipeline Tool will automatically export all records of the targeted record group type, regardless of who created them.

To export (and save in a DB file) records that were created by a certain user or users (`-u` or `--user`), run the following:

```shell
$ heurist dump -u 2 -u 3 -u 4 -f DATABASE.db
```

## Record

```console
Usage: heurist record [OPTIONS]

  Get a JSON export of a certain record type.

Options:
  -t, --record-type INTEGER  The ID fo the record type  [required]
  -o, --outfile PATH         JSON file path.
  --help                     Show this message and exit.
```


## Schema

```console
Usage: heurist schema [OPTIONS]

  Command to export documentation              about the database schema.

Options:
  -t, --output-type [csv|json]  Data format in which the schema will be
                                described.     csv = 1 CSV file for each
                                record type. json = 1 file that     lists all
                                records together  [required]
  -r, --record-group TEXT       Group name of the record types to be
                                described.         Can be declared multiple
                                times for multiple groups.  [default: My
                                record types]
  -o, --outdir DIRECTORY        Path to the directory in which the files will
                                be written.         Defaults to name of the
                                database + '_schema'.
  --help                        Show this message and exit.
```