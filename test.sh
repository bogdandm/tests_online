#!/usr/bin/env bash

cd tests_online_docker
docker-compose build
docker-compose up -d
docker exec tests-online-django bash -c "cd tests_online && ./manage.py test"