#!/usr/bin/env bash

mkdir -p /mnt/static/_frontend-app/
cp -R /opt/tests_online/build/* /mnt/static/_frontend-app/
rm -rf /mnt/static/frontend-app/
mv /mnt/static/_frontend-app /mnt/static/frontend-app