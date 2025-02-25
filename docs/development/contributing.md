# Contributing File

## VS Code settings

```json
{
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
    "flake8.args": [
            "--max-line-length", "88",
            "--extend-ignore", "E203"
        ],
    "black-formatter.args": [
        "--line-length", "88"
    ],
    "isort.args": [
        "--line_length", "88",
        "--wrap-length", "88"
    ],
    "editor.defaultFoldingRangeProvider": "ms-python.black-formatter",
    "isort.check": true
}
```

## Dependency / publishing manager

Install `poetry`.

```shell
pip install --upgrade pip
pip install poetry
```

Using poetry, install the package for development.

```shell
poetry install
```

## Linting

`poetry run flake8`

```console
$ poetry run flake8 --extend-exclude ./examples --max-line-length 88

./heurist/examples/file/single.py:8:89: E501 line too long (120 > 88 characters)
./heurist/examples/geo/single.py:16:89: E501 line too long (79411 > 88 characters)
```

## Testing

`poetry run pytest`

```console
$ poetry run pytest
===================== test session starts =====================
platform darwin -- Python 3.12.2, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/kellychristensen/Dev/LostMa/heurist-api
configfile: pytest.ini
testpaths: tests, heurist/src
plugins: anyio-4.8.0
collected 50 items

tests/integration/dump_test.py .                                         [  2%]
tests/unit/api_client/client_test.py ....                                [ 10%]
tests/unit/database/database_test.py .                                   [ 12%]
tests/unit/database/modeling_test.py .                                   [ 14%]
tests/unit/database/skeleton_test.py .                                   [ 16%]
tests/unit/heurist_transformers/detail_converter_test.py .......         [ 30%]
tests/unit/heurist_transformers/dynamic_pydantic_data_field_test.py .... [ 38%]
..                                                                       [ 42%]
tests/unit/heurist_transformers/prepare_records_test.py ........         [ 58%]
tests/unit/heurist_transformers/record_modeler_test.py ......            [ 70%]
heurist/src/api_client/client.py F.                                      [ 74%]
heurist/src/api_client/url_builder.py ...                                [ 80%]
```
