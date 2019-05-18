#!/usr/bin/env bash

./docker_push.sh $1

ssh -o "StrictHostKeyChecking no" -tt -i /tmp/id_rsa root@bogdandm.xyz << EOF
    cd /opt/tests_online/tests_online_docker
    git pull
    docker-compose pull
    docker-compose up -d
EOF