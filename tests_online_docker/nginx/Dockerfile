FROM nginx:latest

RUN apt-get update
RUN apt-get -y install curl
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /opt/wait-for-it.sh
RUN chmod +x /opt/wait-for-it.sh

RUN rm /etc/nginx/conf.d/*
COPY nginx/* /etc/nginx/conf.d/
RUN mkdir -p /etc/nginx/ssl/
COPY nginx/ssl/* /etc/nginx/ssl/