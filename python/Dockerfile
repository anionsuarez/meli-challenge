FROM python:3.5-alpine

RUN apk add --update \
    mariadb-dev \
    build-base

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./scrap-gmail.py" ]