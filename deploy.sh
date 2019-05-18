#!/usr/bin/env bash

./docker_push.sh $1

ssh -o "StrictHostKeyChecking no" -T -i /tmp/id_rsa root@bogdandm.xyz << EOF
    cd /opt/tests_online/tests_online_docker
    git pull && \
    docker-compose -f docker-compose.yml -f docker-compose-production.yml pull && \
    docker-compose -f docker-compose.yml -f docker-compose-production.yml up -d
EOF