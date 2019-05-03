FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/tests_online/
WORKDIR /opt/tests_online/

RUN apk add --no-cache --update \
    build-base \
    linux-headers \
    python3-dev \
    bash \
    jpeg-dev \
    zlib-dev \
    postgresql-dev \
    pcre-dev \
    && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip && pip install pipenv

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /opt/tests_online/wait-for-it.sh
RUN chmod +x wait-for-it.sh

COPY Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile --dev

COPY . ./