# Publishing Versions

[I found this blog helpful.](https://hermann-web.github.io/blog/blog/2024/03/16/publishing-your-python-project-with-poetry/#configuring-poetry-one-time-setup)

## Configure PyPI authentication

If you haven't already, configure your PyPI authentication using your API key for that package.

```shell
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry config pypi-token.test-pypi pypi-YYYYYYYY
```

## Tests

When you're ready to publish a new version of the package to PyPI, run all the tests.

```shell
poetry run pytest
```

## Update

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

## Commit

With a message indicating the new version (i.e. `v0.0.0`) updated in the `pyproject.toml`, commit the file's changes.

```shell
git commit -m "bump v0.0.0"
```

Build a distribution of the package with the new version name.

```shell
poetry build
```

## Push & Publish

Tag and push the commit to GitHub.

```shell
git tag v0.0.0
git push origin v0.0.0
```

Publish the committed package to PyPI.

```shell
poetry publish -r test-pypi
```
