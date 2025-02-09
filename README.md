![count of tests](./docs/assets/tests-badge.svg)
![test coverage](./docs/assets/coverage-badge.svg)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

<img src="./docs/assets/logo-transparent-1.png" style="width:300px" alt="Logo showing heurist on the left, a pipe in the middle, and output formats DuckDB, JavaScript and CSV on the right."/>

# Heurist ETL Pipeline

Extract, transform, and load data from your Heurist* database into local formats. Great for freeing up your data analysis!

\* Currently, this project's API only supports Heurist databases hosted on HumaNum's servers and requires the login credentials of someone with access to the database.

- [Purpose](#purpose)
- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Usage](./docs/AdvancedUsage.md) (separate page)
- [Contributing](./docs/ContributingFile.md) (separate page)
- [Further Resources](#further-resources)
- [License](#license)
- [Funding](#funding)

## Purpose

Heurist is a low-code, server-based solution to help researchers Create, Read, Update, and Delete records (aka, perform CRUD operations) in a relational database framework. In order to help non-technical users (i.e. historians, archeologists) quickly get to work entering and visualising their relational data, Heurist introduces a lot of complexity behind the scenes.

But what about when you want to analyse the data you've entered? Or even integrate it with other parts of a data pipeline?

Heurist is a good Online Transaction Processing (OLTP) database, but it's not such a great Online Analytic Processing (OLTP) database. You know what is great for analysis? [DuckDB](https://duckdb.org/) ! Many modern data science tools integrate seamlessly with DuckDB. Plus it has a great [Python client](https://duckdb.org/docs/api/python/overview), which also allows analysts to interact with their data in Jupyter notebooks.

This tool extracts, transforms, and loads your Heurist data in a local DuckDB database. You can then optionally export the loaded data into CSV files. Lastly, you can export a summary of your Heurist database's schema as a JSON file. As we've done in the LostMa project, such a comprehensive and simplified summary can be parsed by JavaScript and integrate into a website, i.e. [https://lostma-erc.github.io/](https://lostma-erc.github.io/corpus/documentation/entities/101).

Final thoughts: This pipeline is most useful at the end of your data entry, when you want to bring your Heurist database down from the clouds and into new stages of analysis and/or development.

## Installation

Required:
- [Python](https://realpython.com/installing-python/) (version 3.12)
- Virtual environment manager (recommended: [`pyenv`](https://github.com/pyenv/pyenv))

Steps:

1. Create a new virtual environment, ideally with the word "heurist" in the title.

2. Activate the virtual environment.

2. Install the pipeline with `pip install git+https://github.com/LostMa-ERC/heurist-api`.

2. Write and save your Heurist login credentials in a `.env` file, directly accesible from where you will run the tool's commands.

`.env`
```
DB_NAME=your_database
DB_LOGIN=your.name
DB_PASSWORD=your-password
```

> Alternatively, you can provide them as options after the command `heurist`, i.e. `heurist -d "your_database" -l "your.name" -p "your-password"`.

4. Test the installation.

```console
Usage: heurist [OPTIONS] COMMAND [ARGS]...

  Group CLI command for connecting to the Heurist DB

Options:
  --version            Show the version and exit.
  -d, --database TEXT  Name of the Heurist database
  -l, --login TEXT     Login name for the database user
  -p, --password TEXT  Password for the database user
  --testing            Whether to run in debug mode, default false.
  --help               Show this message and exit.

Commands:
  dump    Command to export data of records of a given record group type.
  record  Get a JSON export of a certain record type.
  schema  Command to export documentation about the database schema.
```

## Basic Usage

Having provided the login credentials, either by declaring each option or having written them in a `.env` file at the root of where you're running the tool, you're ready to export your records.

```shell
$ heurist dump -f DATABASE.db
```
All `dump` commands, even when exporting CSV files, require you to save the results in a DuckDB database file. Declare that file with the option `-f` and the name of the `.db` file you want to create or update.

It also creates a `./logs` directory and generates 2 log files. One, `heurist.db.log`, logs warnings about records in your Heurist database that do not match the structure you've declared in Heurist. Until these errors are corrected in Heurist, these records will not be loaded into the DuckDB database.

The other log file, `tables.log.tsv`, is a summary of the schemas of the tables created in the DuckDB database. See the example lines below, which show the columns of a table named `TextTable`.

```tsv
TableName	ColumnName	DataType
TextTable	H-ID	<class 'int'>
TextTable	type_id	<class 'int'>
TextTable	preferred_name	typing.Optional[str]
TextTable	language_COLUMN	typing.Optional[str]
TextTable	language_COLUMN TRM-ID	typing.Optional[int]
TextTable	literary_form	typing.Optional[str]
TextTable	alternative_names	list[typing.Optional[str]]
TextTable	is_expression_of H-ID	typing.Optional[int]
```

When you parse the tab-separated-values (TSV) log file shown above, you'll get the following:

|TableName|ColumnName|DataType|
|--|--|--|
|TextTable|H-ID|<class 'int'>|
|TextTable|type_id|<class 'int'>|
|TextTable|preferred_name|typing.Optional[str]|
|TextTable|language_COLUMN|typing.Optional[str]|
|TextTable|language_COLUMN TRM-ID|typing.Optional[int]|
|TextTable|alternative_names|list[typing.Optional[str]]|
|TextTable|is_expression_of H-ID|typing.Optional[int]|

It is important to note several ways this pipeline transforms and simplifies the Heurist database's nested relational tables.

- ex. `typing.Optional[...]`: Optional data fields are indicated with `typing.Optional`, whereas required data fields directly have a data type, i.e. `<class int>`.
- ex. `_COLUMN`: When your record's data field uses a name reserved for other purposes in SQL, i.e. "language," the suffix `_COLUMN` is appeneded to it.
- ex. `TRM-ID`: Vocabulary terms are repeated twice in the transformed DuckDB table. First, the term itself is directly available in the column named after the data field. Second, a unique identifier for the term is given in a column with the same name as the first but modified with the suffix `TRM-ID`. Use this ID to join on the `trm` table and get more metadata about the vocabulary term.
- ex. `list[typing.Optional[...]]`: When a data field can be repeated on a record, its value in the transformed DuckDB table is a list.

## Further Resources

This pipeline is part of a continuous integration workflow on the LostMa project's [website](https://lostma-erc.github.io/corpus). It is periodically deployed to update analyses and the summary of the database's schema.

- [LostMa ERC website](https://lostma-erc.github.io/corpus)

## License
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## Funding

The development of this pipeline tool was funded by the European Research Council. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.
