#!/usr/bin/env bash

python3 ./tests_online/manage.py collectstatic --no-input
uwsgi --yaml ./tests_online_docker/django/uwsgi.yml