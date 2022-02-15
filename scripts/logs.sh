#!/bin/bash

docker-compose -f development.yml logs -t $1
