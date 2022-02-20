#!/bin/bash

docker-compose -f development.yml down -v
sudo rm -rf data
find . -type d \( -name venv -o -name postgres \) -prune -false -o -path '*/migrations/*.py*' -not -name  "__init__.py" -exec rm -f {} +