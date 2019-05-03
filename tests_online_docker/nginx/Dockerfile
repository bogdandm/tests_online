FROM nginx:1.15-alpine

RUN apk add --update --no-cache \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /opt/wait-for-it.sh
RUN chmod +x /opt/wait-for-it.sh

RUN rm /etc/nginx/conf.d/*
RUN mkdir -p /etc/nginx/ssl/

COPY nginx/* /etc/nginx/conf.d/
COPY nginx/ssl/* /etc/nginx/ssl/