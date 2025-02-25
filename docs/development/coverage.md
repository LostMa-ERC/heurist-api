# Badges

> Warning: This documentation is under development.

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
