# BUILDER
FROM python:3.7-buster as builder
MAINTAINER Nakashi

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

RUN apt-get update && \
      apt-get install -y \
      build-essential libssl-dev libffi-dev libblas3 \
      libc6 liblapack3 gcc libc-dev musl-dev \
      python3-dev postgresql-client netcat

RUN pip install --upgrade pip
COPY . .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# FINAL
FROM python:3.7-buster

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static && mkdir $APP_HOME/media
WORKDIR $APP_HOME

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh $APP_HOME

COPY . $APP_HOME

RUN adduser app
RUN chown -R app:app $APP_HOME
USER app
