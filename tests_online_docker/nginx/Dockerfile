FROM nginx:latest

RUN rm /etc/nginx/conf.d/*
COPY nginx/* /etc/nginx/conf.d/
RUN mkdir -p /etc/nginx/ssl/
COPY nginx/ssl/* /etc/nginx/ssl/