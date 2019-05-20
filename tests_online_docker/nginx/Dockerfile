FROM nginx:1.15-alpine

RUN apk add --update --no-cache \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /opt/wait-for-it.sh
RUN chmod +x /opt/wait-for-it.sh

# Get rid of default setup
RUN rm /etc/nginx/conf.d/*
RUN rm -rf /etc/nginx/nginx.conf

ARG ROOT_CONF=nginx.conf
COPY nginx/* /etc/nginx/conf.d/
RUN echo "include \"/etc/nginx/conf.d/${ROOT_CONF}\";" > /etc/nginx/nginx.conf