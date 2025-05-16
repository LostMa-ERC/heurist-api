# Publishing Versions

It is recommended to use the automated workflow for releasing new versions of the package to Test PyPI.

1. Finish pull requests to the main branch and/or push your changes to the main branch. Make sure all changes you want in the new release are committed and pushed.

2. Update the package version according to semantic versioning practices. This will modify the `pyproject.toml` file. If using `uv`, you can do the following:

    - `uv version --bump patch`
    - `uv version --bump minor`
    - `uv version --bump major`

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
