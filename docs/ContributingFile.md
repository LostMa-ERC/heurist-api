# Contributing File

## Dependency / publishing manager

Install `poetry`.

```shell
pip install --upgrade pip
pip install poetry
```

Using poetry, install the package.

```shell
poetry install
poetry env activate
```

## Linting

- `flake8` (install independently), ^7.1

```shell
flake8 --extend-exclude ./examples --max-line-length 88
```

Relevant VSCode settings.

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

## Testing

- `pytest` (required in `pyproject.toml`), ^8.1

Run tests in all code, `src/` and `tests/`.

```shell
pytest --log-disable=""
```

## Badges

- `coverage` (install independently), ^7.6
- `genbadge` (install insependently), ^1.1

```shell
pip install genbadge[all]
```

Coverage badge:

```shell
coverage run -m pytest
coverage xml
genbadge coverage -i coverage.xml
mv coverage-badge.svg ./docs/assets
rm coverage.xml
```

Tests badge:

```shell
pytest --junitxml=reports/junit/junit.xml
genbadge tests
mv tests-badge.svg ./docs/assets
```

## Working locally via poetry

```shell
poetry lock
poetry install
pip install heurist
```

## [Publishing new versions](https://hermann-web.github.io/blog/blog/2024/03/16/publishing-your-python-project-with-poetry/#configuring-poetry-one-time-setup)

### Configuration

```shell
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi pypi-YYYYYYYY
```

### Action

Lock in any big changes.

```shell
poetry lock
```

Update the version.

```shell
poetry version prerelease
# or
poetry version patch
# or
poetry version minor
# or
poetry version major
```

```shell
poetry build
poetry publish -r test-pypi
```
