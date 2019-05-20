#!/usr/bin/env bash

docker exec test-online-certbot certbot certonly \
    --webroot \
    --email bogdan.dm1995@yandex.ru \
    --no-eff-email \
    --agree-tos \
    --webroot-path=/etc/certbot \
    -d tests.bogdandm.xyz
