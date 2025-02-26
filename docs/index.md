# Heurist ETL

[![Python package](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml/badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml) [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![coverage](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/coverage-badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/coverage-badge.svg)
[![tests](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/tests-badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/tests-badge.svg)

This Python package Extracts, Transforms, and Loads (ETL) data from a Heurist database server into a local [DuckDB](https://duckdb.org) database file.

## Commands

* `heurist download -f [file]` - Load all the records of a certain record group type into a DuckDB database file. There is also the option to export the transformed tables into CSV files for each record type.
* `heurist record -t [record-type]` - Simply calling Heurist's API, export all of a targeted record type's records to a JSON file.
* `heurist schema -t [output-type]` - Transform a Heurist database schema into descriptive CSV tables for each record type or into a descriptive JSON array.

Learn how to install and start using the `heurist` Command-Line Interface (CLI) on the [Usage](usage/index.md) page.

> _Note: Currently, the _`heurist`_ package has only been developed for Heurist databases hosted on [Huma-Num's Heurist server](https://heurist.huma-num.fr/heurist/startup/). This includes nearly 2000 database instances, which is a good place to start! If you want to help develop the API client to work with other servers, consider [contributing](development/contributing.md)._

---

## Project layout

    heurist/
        api/            # Python client for Heurist API
        cli/            # Commands for CLI tool
        converters/     # Methods and functions for transforming Heurist data
        database/       # DuckDB database for loading data
        mock_data/      # Examples of data structures exported from Heurist API
        models/         # Pydantic models for parsing exported Heurist data
        schema/         # Tools for transforming database structure into schema documentation
        sql/            # SQL scripts for manipulating and transforming Heurist data
