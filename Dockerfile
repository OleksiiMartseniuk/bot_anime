FROM python:3.10.4-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev nano

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt


COPY . /app/