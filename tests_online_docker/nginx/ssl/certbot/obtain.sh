#!/usr/bin/env bash

docker exec tests-online-certbot certbot certonly \
    --webroot \
    --email bogdan.dm1995@yandex.ru \
    --no-eff-email \
    --agree-tos \
    --webroot-path=/etc/certbot \
    -d tests.bogdandm.xyz
