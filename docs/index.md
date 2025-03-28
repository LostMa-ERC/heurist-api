# Heurist ETL

[![Python package](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml/badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml) [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![coverage](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/coverage-badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/coverage-badge.svg)
[![tests](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/tests-badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/tests-badge.svg)

This Python package Extracts, Transforms, and Loads (ETL) data from a Heurist database server into a local [DuckDB](https://duckdb.org) database file.

- [Installation & configuration](usage/index.md#installation)
- [Basic command-line usage](usage/index.md#cli-commands)
- [Integrate API client in Python code](usage/module.md)
- [Load Heurist data into R-studio](usage/rstudio.md)

[![Logo](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/logo-transparent-1.png)](https://github.com/LostMa-ERC/heurist-etl-pipeline/raw/main/docs/assets/logo-transparent-1.png)

```shell
$ pip install \
--index-url https://test.pypi.org/simple/ \
--extra-index-url https://pypi.org/simple \
heurist
```

## Commands

- `heurist download -f [file]` - Load all the records of a certain record group type into a DuckDB database file. There is also the option to export the transformed tables into CSV files for each record type.
- `heurist record -t [record-type]` - Simply calling Heurist's API, export all of a targeted record type's records to a JSON file.
- `heurist schema -t [output-type]` - Transform a Heurist database schema into descriptive CSV tables for each record type or into a descriptive JSON array.

> _Note: Currently, the _`heurist`_ package has only been developed for Heurist databases hosted on [Huma-Num's Heurist server](https://heurist.huma-num.fr/heurist/startup/). This includes nearly 2000 database instances, which is a good place to start! If you want to help develop the API client to work with other servers, consider [contributing](development/contributing.md)._

---

## ERC-funded project

This Python package is distributed with the [Creative Commons' Attribution-ShareAlike 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).

It was developed as part of a [project](https://doi.org/10.3030/101117408) funded by the European Research Council. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.
