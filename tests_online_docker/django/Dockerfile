FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install procmail less nano
RUN pip install pipenv

RUN mkdir /opt/tests_online/
WORKDIR /opt/tests_online/
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile
COPY . ./