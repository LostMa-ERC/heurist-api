# Publishing Versions

## Automated workflow

It is recommended to use the automated workflow for releasing new versions of the package to PyPI.

1. Finish pull requests to the main branch and/or push your changes to the main branch. Make sure all changes you want in the new release are committed and pushed.

2. Locally, use `poetry` to update the package version according to semantic versioning practices. This will modify the `pyproject.toml` file.

    - `poetry version prerelease`
    - `poetry version patch`
    - `poetry version minor`
    - `poetry version major`

3. Track the modified `pyproject.toml` file in git.

    - `git add pyproject.toml`.

4. Commit the updated `pyproject.toml` file; the message starts with `bump` and indicates the new version number.

    - For example: `git commit -m "bump v0.0.0"`.

5. Push the finalised `pyproject.toml` to the repository.

    - `git push`

6. Create a tag for the new version, starting with `v`.

    - For example: `git tag v0.0.0`

7. Push the tag to the repository.

    - For example: `git push origin v0.0.0`

8. Pushing a tag that starts with `v` will trigger the workflow [`pypi-release.yml`](https://github.com/LostMa-ERC/heurist-etl-pipeline/blob/main/.github/workflows/pypi-release.yml)

## Manual workflow

> _Note: I used [this blog post](https://hermann-web.github.io/blog/blog/2024/03/16/publishing-your-python-project-with-poetry/#configuring-poetry-one-time-setup) to design this workflow._

### Configure PyPI authentication

If you haven't already, configure your PyPI authentication using your API key for that package.

```shell
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi pypi-YYYYYYYY
```

### Run tests

When you're ready to publish a new version of the package to PyPI, run all the tests.

```shell
poetry run pytest
```

### Update the package dependencies

Lock in any changes that have been made to the package's scripts and/or dependencies.

```shell
poetry lock
```

Update the package version.

```shell
poetry version prerelease
# or
poetry version patch
# or
poetry version minor
# or
poetry version major
```

### Commit the changes

With a message indicating the new version (i.e. `v0.0.0`) updated in the `pyproject.toml`, commit the file's changes.

```shell
git add pyproject.toml
git commit -m "bump v0.0.0"
```

Build a distribution of the package with the new version name.

```shell
poetry build
```

### Push & publish

Tag and push the commit to GitHub.

```shell
git tag v0.0.0
git push origin v0.0.0
```

Publish the committed package to PyPI.

```shell
poetry publish -r test-pypi
```
