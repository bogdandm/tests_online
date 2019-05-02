FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install procmail less nano
RUN pip install pipenv

RUN mkdir /opt/tests_online/
WORKDIR /opt/tests_online/
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile --dev
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /opt/tests_online/wait-for-it.sh
RUN chmod +x wait-for-it.sh
COPY . ./