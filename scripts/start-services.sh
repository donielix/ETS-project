#!/bin/bash

docker-compose -f development.yml down -v
sudo chown -R $USER:$USER . &&
docker-compose -f development.yml up -d --build $1 &&
docker-compose -f development.yml exec backend bash