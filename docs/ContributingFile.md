# Contributing File

## Linting

- `flake8` (install independently), ^7.1

```shell
$ flake8 --extend-exclude ./examples --max-line-length 88
```

Relevant VSCode settings.

```json
{
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true,
        },
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "ms-python.black-formatter",
    },
    "flake8.args": [
            "--max-line-length", "88",
            "--extend-ignore", "E203"
        ],
    "black-formatter.args": [
        "--line-length", "88",
    ],
    "isort.args": [
        "--line_length", "88",
        "--wrap-length", "88"
    ],
    "editor.defaultFoldingRangeProvider": "ms-python.black-formatter",
    "isort.check": true,
}
```

## Testing

- `pytest` (required in `pyproject.toml`), ^8.1

Run tests in all code, `src/` and `tests/`.

```shell
$ pytest
```

## Badges

- `coverage` (install independently), ^7.6
- `genbadge` (install insependently), ^1.1

```shell
$ pip install genbadge[all]
```

Coverage badge:

```shell
$ coverage run -m pytest
$ coverage xml
$ genbadge coverage -i coverage.xml
$ mv coverage-badge.svg ./assets
$ rm coverage.xml
```

Tests badge:

```shell
$ pytest --junitxml=reports/junit/junit.xml
$ genbadge tests
$ mv tests-badge.svg ./assets
```
