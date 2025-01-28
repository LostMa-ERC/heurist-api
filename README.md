# Heurist Data Pipeline Tool
![logo](./assets/logo-transparent-1.png)

The Heurist Data Pipeline Tool sets you up to manipulate, transform, and/or analyse data in a Heurist* database. It performs an Extract, Transform, Load (ETL) process that delivers the data in an analysis-friendly format.

\* Currently, the ETL process's API only supports Heurist databases hosted on HumaNum's servers and requires the login credentials of someone with access to the database.

## Why build this?

Heurist is a low-code, server-based solution to help researchers Create, Read, Update, and Delete records (aka, perform CRUD operations) in a relational database framework. In order to help non-technical users (i.e. historians, archeologists) quickly get to work entering and visualising their relational data, Heurist introduces a lot of complexity behind the scenes.

But what about when you're done updating your database, and you want to analyse it? Or even integrate it with other parts of your data pipeline?

Heurist is a good Online Transaction Processing (OLTP) database, but it's not such a great Online Analytic Processing (OLTP) database. You know what is great for analysis? [DuckDB](https://duckdb.org/)! Many modern data science tools integrate seamlessly with DuckDB. Plus it has a great [Python client](https://duckdb.org/docs/api/python/overview), which also allows analysts to interact with their data in Jupyter notebooks.

The Heurist Data Pipeline Tool tool extracts, transforms, and loads your Heurist data in a local DuckDB database. You can then optionally export the loaded data in CSV files. Lastly, you can also export a summary of your Heurist database's schema as a JSON file, which can be parsed by JavaScript and integrated into a website, i.e. [https://lostma-erc.github.io/](https://lostma-erc.github.io/corpus/documentation/entities/101).

Final thoughts: This tool is most useful at the end of your data entry, when you want to bring your Heurist database down from the clouds and into new stages of analysis and/or development.

## What do I need?

1. Install the Heurist Data Pipeline Tool in a new virtual Python environment (version 3.12 or greater) with `pip install git+https://github.com/LostMa-ERC/heurist-api`.

2. Write and save your Heurist login credentials in a `.env` file, directly accesible from where you will run the tool.

`.env`
```
DB_NAME=your_database
DB_LOGIN=your.name
DB_PASSWORD=your-password
```

> Alternatively, you can provide them as options after the command `heurist`, i.e. `heurist -d "your_database" -l "your.name" -p "your-password"`.

## How do I get my data?

Having provided the login credentials, either by declaring each option or having written them in a `.env` file at the root of where you're running the tool, you're ready to export your records.

### Export to DB file

To export your records from the Heurist database, saving them  in a DuckDB SQL database file, run the following:

```shell
$ heurist dump -f DATABASE.db
```

### Export to CSV files

To export your records to a DuckDB SQL database and save the tables as CSV files in a directory (`OUTDIR/`), run the following:

```shell
$ heurist dump -f DATABASE.db -o OUTDIR
```

### Export a specific record type group

When you don't declare a `--record-group`, the Heurist Data Pipeline Tool will automatically export all of the databse's records that are of the types declared in the group "My record types."

To export (and save in a DB file) records from your record types and another group, run the following:

```shell
$ heurist dump --record-group "My record types" --record-group "Bibliography" -f DATABASE.db
```

### Export a specific user's records

When you don't declare a specific `--user`, the Heurist Data Pipeline Tool will automatically export all records of the targeted record group type, regardless of who created them.

To export (and save in a DB file) records that were created by a certain user or users (`-u` or `--user`), run the following:

```shell
$ heurist dump -u 2 -u 3 -u 4 -f DATABASE.db
```
