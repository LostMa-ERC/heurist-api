# Heurist Pipeline

[![Python package](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml/badge.svg)](https://github.com/LostMa-ERC/heurist-etl-pipeline/actions/workflows/python-package.yml) [![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

## Commands

* `heurist load -f [file]` - Load records from Heurist into a DuckDB file.
* `heurist record -t [record-type]` - Export records of a certain type in a JSON file.
* `heurist schema -t [output-type]` - Transform and load Heurist schema 
* `mkdocs -h` - Print help message and exit.

## Project layout

    heurist/
        __main__.py # Endpoint for the CLI utility
        src/
            