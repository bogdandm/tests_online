#!/usr/bin/env bash

TRAVIS_TAG=$1
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
declare -a images=("tests-online-frontend" "tests-online-django" "tests-online-nginx")

# Unstable images will be pushed as :unstable,
# everything else as :latest, :unstable and :$TRAVIS_TAG
for image in "${images[@]}"
do
   docker tag $image bogdandm/$image:$TRAVIS_TAG
   docker push bogdandm/$image:$TRAVIS_TAG
   if [ $TRAVIS_TAG != "unstable" ]; then
       docker tag $image bogdandm/$image:unstable
       docker push bogdandm/$image:unstable
       docker tag $image bogdandm/$image:latest
       docker push bogdandm/$image:latest
   fi
done