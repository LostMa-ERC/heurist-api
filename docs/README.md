# Heurist ETL Pipeline

[![Python package](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml/badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml)

Extract, transform, and load data from your Heurist* database into local formats. Great for freeing up your data analysis!

\* Currently, this project's API only supports Heurist databases hosted on HumaNum's servers and requires the login credentials of someone with access to the database.

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [License](#license)
- [Funding](#funding)

## Requirements

- [Python](https://realpython.com/installing-python/) (version 3.12)
- Virtual environment manager (recommended: [`pyenv`](https://github.com/pyenv/pyenv))

## Installation

1. Create a new virtual environment, ideally with the word "heurist" in the title.

2. Activate the virtual environment.

3. Install the latest version.

```shell
pip install \
--index-url https://test.pypi.org/simple/ \
--extra-index-url https://pypi.org/simple \
heurist
```

## Basic Usage

```shell
heurist -d DATABASE_NAME -l "USER.NAME" -p "YOUR-PASSWORD" dump -f DATABASE.db
```

All `dump` commands, even when exporting CSV files, require you to save the results in a DuckDB database file. Declare that file with the option `-f` and the name of the `.db` file you want to create or update.

It also creates a `./logs` directory and generates 2 log files.

### Log 1

`heurist.db.log` logs warnings about records in your Heurist database that do not match the structure you've declared in Heurist. Until these errors are corrected in Heurist, these records will not be loaded into the DuckDB database.

### Log 2

`tables.log.tsv` is a summary of the schemas of the tables created in the DuckDB database. See the example lines below, which show the columns of a table named `TextTable`. When you parse the tab-separated-values (TSV) log file, you'll get the following:

|TableName|ColumnName|DataType|
|--|--|--|
|TextTable|H-ID|<class 'int'>|
|TextTable|type_id|<class 'int'>|
|TextTable|preferred_name|typing.Optional[str]|
|TextTable|language_COLUMN|typing.Optional[str]|
|TextTable|language_COLUMN TRM-ID|typing.Optional[int]|
|TextTable|alternative_names|list[typing.Optional[str]]|
|TextTable|is_expression_of H-ID|typing.Optional[int]|

It is important to note several ways this pipeline transforms and simplifies the Heurist database's complexly related tables.

- ex. `typing.Optional[...]`: Optional data fields are indicated with `typing.Optional`, whereas required data fields directly have a data type, i.e. `<class int>`.
- ex. `_COLUMN`: When your record's data field uses a name reserved for other purposes in SQL, i.e. "language," the suffix `_COLUMN` is appended to it.
- ex. `TRM-ID`: Vocabulary terms are repeated twice in the transformed DuckDB table. First, the term itself is directly available in the column named after the data field. Second, a unique identifier for the term is given in a column with the same name as the first but modified with the suffix `TRM-ID`. Use this ID to join on the `trm` table and get more metadata about the vocabulary term.
- ex. `list[typing.Optional[...]]`: When a data field can be repeated on a record, its value in the transformed DuckDB table is a list.
- ex. `... H-ID`: When a data field is a foreign key that references another table, that column name has the suffix `H-ID`. This is useful if you want to re-import this data field into Heurist, which requires all foreign-key columns to have this suffix.

## License

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## Funding

The development of this pipeline tool was funded by the European Research Council. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.
