FROM python:3.5-alpine

RUN apk add --update \
    mariadb-dev \
    build-base
# Packages that we need 
COPY requirements.txt /app/
WORKDIR /app
# instruction to be run during image build
RUN pip install -r requirements.txt
# Copy all the files from current source duirectory(from your system) to
# Docker container in /app directory 
COPY . /app

CMD [ "python", "./scrap-gmail.py" ]
# CMD [ "python", "./testsql.py" ]
