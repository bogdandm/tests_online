FROM node:8-alpine

ARG REACT_APP_DOMAIN=http://localhost:8000
RUN mkdir /opt/tests_online/
WORKDIR /opt/tests_online/

RUN apk add --no-cache --update \
    bash \
    git \
    && rm -rf /var/cache/apk/*

COPY tests_online_frontend/tests-online-app/yarn.lock ./
COPY tests_online_frontend/tests-online-app/package.json ./
RUN yarn install --pure-lockfile && rm -rf /root/.yarn-cache

COPY tests_online_docker/frontend/move_compiled_files.sh ./
RUN chmod +x ./move_compiled_files.sh
COPY tests_online_frontend/tests-online-app/public ./public/
COPY tests_online_frontend/tests-online-app/src ./src/

RUN REACT_APP_DOMAIN=$REACT_APP_DOMAIN yarn build
RUN rm -rf ./src && rm -rf ./public && rm -rf ./node_modules