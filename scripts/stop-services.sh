#!/bin/bash

docker-compose -f development.yml down -v --remove-orphans
docker-compose -f development.yml rm -f -v