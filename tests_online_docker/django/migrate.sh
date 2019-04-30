#!/usr/bin/env bash

python3 ./tests_online/manage.py collectstatic --no-input
python3 ./tests_online/manage.py migrate --no-input
python3 ./tests_online/manage.py init