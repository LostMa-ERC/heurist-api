#!/bin/bash

# Coverage badge
coverage run -m pytest
coverage xml
genbadge coverage -i coverage.xml
mv coverage-badge.svg docs/assets
rm .coverage
rm coverage.xml

# Update
pytest --junitxml=reports/junit/junit.xml
genbadge tests
mv tests-badge.svg docs/assets
rm -r reports