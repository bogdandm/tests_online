#!/usr/bin/env bash

TRAVIS_TAG=$1
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
declare -a images=("tests-online-frontend" "tests-online-django" "tests-online-nginx")

for image in "${images[@]}"
do
   docker tag $image bogdandm/$image:latest
   docker tag $image bogdandm/$image:$TRAVIS_TAG
   docker push bogdandm/$image:latest
   docker push bogdandm/$image:$TRAVIS_TAG
done