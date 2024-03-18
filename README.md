# Heurist API

Development of Heurist API.

## Install development branch

```console
$ git clone https://github.com/LostMa-ERC/heurist-api.git
$ git checkout dev
$ pip install git+https://github.com/LostMa-ERC/heurist-api.git
```

## Linter

```
pylint heurist_api
```


## Run tests

1. Test the URL builder.

```console
$ python -m doctest src/heurist_api/url_builder.py
```

2. Test the API calls.

```console
$ python -m pytest tests/test_client.py
```

3. Test the database structure parser.

```shell
# to do
```