# Usage

This package's primary use is as a command-line interface (CLI). It's meant to efficiently extract, transform, and load data from their Heurist database into local CSV, JSON, and DuckDB files.

Secondarily, you can also exploit certain modules, such as the API client, for your own Python development. For this secondary use, read the documentation [here](./recipes/module.md).

## Installation (all purposes)

### Requirements

- Python version 3.10 or greater
- Virtual Python environment, i.e. [`pyenv`](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).

### Steps

1. If you don't have Python installed on your machine, download version 3.10 or greater.
    - Need help installing Python? Check out the [Real Python](https://realpython.com/installing-python/) blog's tutorial.
2. Create a new virtual environment for the package. Then activate it.
    - What's the simplest way? Check out [Real Python](https://realpython.com/python-virtual-environments-a-primer/)'s thorough blog post.
    - I recommend naming the environment `heurist`.
3. Use `pip install` to install the `heurist` Python package.

```console
$ pip install \
--index-url https://test.pypi.org/simple/ \
--extra-index-url https://pypi.org/simple \
heurist
```

## Configure the CLI

All of the `heurist` subcommands require connecting to your Heurist database.

### Option 1: Manually declare login credentials

After the `heurist` command, provide the Heurist database name (`--database`, `-d`) as well as the username (`--login`, `-l`) and password (`--password`, `-p`) for a user with access to the Heurist database.

```console
$ heurist -d YOUR_DATABASE -l "your.username" -p "your-password"
```

### Option 2: Set environment variables

From wherever you're running the command in the terminal, create a `.env` file.

```console
$ touch .env
```

Then, using some kind of simple text editor (and replacing the defaults with your login credentials), add the following 3 lines to the `.env` file:

```shell
DB_NAME=your_database
DB_LOGIN=your.username
DB_PASSWORD=your-password
```

With the `.env` file, you can run any `heurist` subcommand without needing to provide any other information.

```shell
$ heurist --help
Usage: heurist [OPTIONS] COMMAND [ARGS]...

  Group CLI command for connecting to the Heurist DB

Options:
  --version            Show the version and exit.
  -d, --database TEXT  Name of the Heurist database
  -l, --login TEXT     Login name for the database user
  -p, --password TEXT  Password for the database user
  --debugging          Whether to run in debug mode, default false.
  --help               Show this message and exit.

Commands:
  download  Export data of records of 1 or more record group types.
  record    Get a JSON export of a certain record type.
  schema    Generate documentation about the database schema.
```

---

## Basic usage

### Download groups of records

```shell
heurist download -f NEW_DATABASE.db
```

By default, without specifying any target record groups, `heurist download` will download all the records you created in the "My record types" group.

```shell
$ heurist download -f NEW_DATABASE.db
Get DB Structure ⠼ 0:00:00
Get Records ━━━━━━━━━━━━ 3/3 0:00:08

Created the following tables
┌───────────────┐
│     name      │
│    varchar    │
├───────────────┤
│ YourRecord_A  │
│ YourRecord_B  │
│ YourRecord_C  │
│ dty           │
│ rst           │
│ rtg           │
│ rty           │
│ trm           │
├───────────────┤
│    18 rows    │
└───────────────┘
```

For full documentation on this subcommand, read the [`Download record groups`](./recipes/download) recipe.

> The lowercase table names are structural tables Heurist uses to keep track of the record types (`rty`, `rtg`), data fields (`dty`, `rst`), and vocabularies (`trm`) you create / modify in Heurist. They're also made available in your download in case you need them.

### Download a record type's records

```console
heurist record -t RECORD_TYPE_ID_NUMBER
```

Specify the targeted record type with the option `-t` or `--record-type`. The subcommand `record` will call Heurist's API and download the type's records in Heurist's JSON export.

```shell
$ heurist record -t 101
Get Records of type 101 ⠋ 0:00:00
Writing results to: RTY_101.json
```

For full documentation on this subcommand, read the [`Export a record type`](./recipes/download) recipe.

### Generate documentation about Heurist's schema

```console
heurist schema -t OUTPUT_TYPE
```

Specify the format in which you want to read the schema, either `csv` or `json`.

```shell
$ heurist schema -t csv
Downloading schemas ⠋ 0:00:04
Describing record types ━━━━━━━━━━━━ 3/3
```

For full documentation on this subcommand, read the [`Generate schema`](./recipes/schema) recipe.
