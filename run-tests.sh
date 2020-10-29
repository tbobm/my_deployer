#!/bin/sh
python -m pytest --color=yes --cov my_deployer --cov-report term tests/
