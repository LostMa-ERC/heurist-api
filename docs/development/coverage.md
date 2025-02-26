# Badges

This repository has 2 generated badges related to testing coverage. They require the `coverage` and `genbadge` Python libraries.

## Set up development environment

In your virtual Python environment, run the following:

```shell
pip install --upgrade pip poetry
poetry install
```

## Generate badges

Run the prepared `gen_badges.sh` script in the `./scripts` directory at the root of the GitHub repository.

```shell
bash ./scripts/gen_badges.sh
```
