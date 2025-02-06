![count of tests](./assets/tests-badge.svg)
![test coverage](./assets/coverage-badge.svg)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

<img src="./assets/logo-transparent-1.png" style="width:300px" alt="Logo showing heurist on the left, a pipe in the middle, and output formats DuckDB, JavaScript and CSV on the right."/>

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

## Further Resources

This pipeline is part of a continuous integration workflow on the LostMa project's [website](https://lostma-erc.github.io/corpus). It is periodically deployed to update analyses and the summary of the database's schema.

- [LostMa ERC website](https://lostma-erc.github.io/corpus)

## License
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## Funding

The development of this pipeline tool was funded by the European Research Council. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.
