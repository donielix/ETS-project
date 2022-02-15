#!/bin/bash

docker-compose -f development.yml exec ${1:-backend} bash