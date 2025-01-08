# Heurist API Client

The Heurist API Client command-line interface (CLI) lets you interact locally, in the form of simple CSV files and a file-based DuckDB database, with data that is stored and structured in a Heurist* database on a remote server.

\* Currently, only Heurist databases hosted on HumaNum's servers are supported.

## Output

After running the dump command, you'll get 2 things:

1. A DuckDB database file with tables for all the relationship markers in the database and all the record types targeted for export.
    - This is useful for conducting data analysis, validation, and enrichment using simple SQL.
    - It's also useful if you want to embed the database file in a website or use with an API.

2. CSV tables for the targeted record types and your database's relationship markers.

## Justification

At its core, Heurist is a relational database. However, when you look under the low-code, user-friendly hood, there's a lot going on. All of a record type's properties are not simple columns in a table. Therefore, exporting your database's records is not as simple as downloading a few CSV files. Heurist, however, does permit some database users to export certain information in the form of CSV files, but the process is meant to be executed from within a broswer and is not optimized for automated workflows.

### Resource field relationships

Let's start with the simplest relation a Heurist record type can have to another record type (or a record of the same type). A record type's **resource field** directly relates the record to another record; this relationship is called a "foreign key" relation in typical relational database terminology. Thus, a single column in the exported record type's table can adequately contain the record type's **resource field** in the Heurist database.

`Record Type 101 : "Works"`
|H-ID|title (text)|author H-ID (resource field)|
|--|-----|--------------|
|01|Book 1|02|

`Record Type 102 : "People"`
|H-ID|author (text)|
|--|------|
|02|Bublik|

### Relationship marker relationships

More complicated are Heurist's **relationship markers**. A relationship marker contains 2 pieces of information in one data field. One is the type of relation, which Heurist calls the "term." You define these in the relationship vocabulary tab. The other is the record that is the target of the relationship. Under the hood, Heurist manages this loaded relationship via the relationship marker record type (ID 1), in an intermediary table. In relational database terminology, we might call Heurist's intermediary table a "relational table."


`Record Type 101 : "Works"`
|H-ID|title (text)|author H-ID (resource field)|
|--|-----|--------------|
|01|Book 1|02|

`Record Type 102 : "People"`
|H-ID|author (text)|responsibility (relationship marker)|
|----|-------------|-------------------|
|02|Bublik|wrote Book 1|
|03|Kotov|edited Book 1|

`Record Type 1 : Relationship Markers`
|source|target|term|
|------|------|----|
|02|01|wrote|
|03|01|edited|

Because the term of a record type's relationship marker can vary, the data is not simply written to a single column on a table. In the example above, the column "responibility" on the `People` table is not very useful in SQL because the bipartite information is stored as a string with no declared syntax. Therefore, our solution removes this column / data field and simply provides the relationship markers table. As an online platform, Heurist is designed to seamlessly manage this complexity inside a single data field, but when flattened to CSV files and tables, it poses a challenge.


## Set up

Install the client in a new virtual Python environment (version 3.12) with `pip install git+https://github.com/LostMa-ERC/heurist-api`.

Save your Heurist login credentials in a `.env` file, directly accesible from where you will run the tool.

`.env`
```
DB_NAME=your_database
DB_LOGIN=your.name
DB_PASSWORD=your-password
```

Alternatively, you can provide them as options after the command `heurist`, i.e. `heurist -d "your_database" -l "your.name" -p "your-password"`.

## Run

Export your records from the database to a DuckDB SQL table.

```shell
$ heurist dump -f DATABASE.db
```

Export your records to a DuckDB SQL table and save the tables as CSV files in a directory (`OUTDIR/`).

```shell
$ heurist dump -f DATABASE.db -o OUTDIR
```

Export records from a record group other than "My record types" and save to a DuckDB SQL table. The default record type group is "My record types," in which most Heurist users define the record types for their database.

```shell
$ heurist dump --record-group "Bibliography" -f DATABASE.db
```

Export records that were created by a certain user or users (`-u` or `--user`).

```shell
$ heurist dump -u 2 -u 3 -u 4 -f DATABASE.db
```
