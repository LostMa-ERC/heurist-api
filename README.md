# Heurist API Client

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