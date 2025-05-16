# Contributing File

> Warning: This documentation is under development.

Overall workflow:

1. From the GitHub repository, open an issue about what you want to contribute.

2. Develop your contribution on the development (`dev`) branch of the git repository.

3. Run linting and tests locally. Affirm that everything is passing.

4. Push changes to the development branch.

5. From the GitHub repository, make a pull request.

---

## Set up

Install the project and set up the environment.

### IDE

If you're using VS Code, apply the example settings.

```console
$ mkdir .vscode
$ cp vscode-settings.example.json .vscode/settings.json
```

### Git & Python

#### Repository

Clone the repository.

```console
$ git clone git@github.com:LostMa-ERC/heurist-etl-pipeline.git
```

#### Virtual Environment

Set up a virtual Python environment and install the package. I recommend using [`uv`](https://docs.astral.sh/uv/), which is what the CI workflows use on GitHub Actions.

```console
$ uv venv --python 3.13
$ source .venv/bin/activate
(venv) $ uv pip install -e .
```

#### Development branch

Move to the git repository's development (`dev`) branch. If you've never worked on the development branch, create it with `checkout -b` instead of `checkout`.

```console
$ git checkout dev
$ git pull
```

---

## Development

Before pushing changes to the repository, locally run linting and testing. These checks will be run again and for all covered Python versions when pushed to the remote repository.

### Style guide

1. Module names are written in snake case.
    - Example: [`record_validator.py`](../reference/validators/record_validator.md)
    - An exception is made for the modules of the `pydantic.BaseXmlModel` models in `heurist/models/structural`, i.e. [`DetailTypes.py`](../reference/models/structural/DetailTypes.md).

2. Classes are written in camel case, i.e. `HeuristAPIClient`.

3. Functions and class methods have docstrings written in Google's format.
    - When describing what the function or method does, the tense is in the imperative, i.e. "Construct a URL from path parameters."
    - When a function or method's parameters can be written in a single line and/or don't depend on complex class instances, write unit tests in the docstring with [`doctest`](https://docs.python.org/3/library/doctest.html).
        - Preface the shell instructions with `Examples:`.
        - On the next line, indent by 4 spaces before the doctest string `>>> 1+1`.

4. The location of test modules depends on whether they're end-to-end (`tests/e2e`), integration (`tests/integration`), or unit tests (`tests/unit`).
    - From the relevant test directory, the test module is placed in a subdirectory named after the package's corresponding subdirectory.
    - For example, a unit test about `heurist/api/client.py` is written in the subdirectory `tests/unit/api`.
    - An exception is made for end-to-end tests, which test CLI commands from the `tests/e2e` directory.

5. Test modules are written in snake case and their name starts with the element being tested, followed by `_test.py` at the end.
    - For example, a unit test about `heurist/api/client.py` is written in `tests/unit/api/client_test.py`

6. Complex SQL queries are written in individual SQL files in the `sql/` directory, i.e. `sql/query.sql`. Then, the query's parsed text is read in the `sql/__init__.py` module and made available as a constant, as follows:

```python
sql_file = Path(__file__).parent.joinpath("query.sql")

with open(sql_file) as f:
    QUERY = f.read()
```

### Linting

```console
$ uv run ruff check src/
```

### Testing

```console
$ uv run pytest
```
