FROM python:3.5-alpine

# Packages that we need 
COPY requirements.txt /app/
WORKDIR /app
# instruction to be run during image build
RUN pip install -r requirements.txt
# Copy all the files from current source duirectory(from your system) to
# Docker container in /app directory 
COPY . /app

CMD [ "python", "./scrap-gmail.py" ]

# ENV PYTHONUNBUFFERED 1
# RUN set -e; \
#         apk add --no-cache --virtual .build-deps \
#                 gcc \
#                 libc-dev \
#                 linux-headers \
#                 mariadb-dev \
#                 python3-dev \
#                 postgresql-dev \
#         ;
# RUN mkdir /melichalenge
# WORKDIR /melichalenge
# # ENV REFRESHED_AT 2017-12-25
# ADD requirements.txt /melichalenge/
# RUN pip install --no-cache-dir -r /melichalenge/requirements.txt
# RUN pip install uwsgi
# ADD . /melichalenge/
# CMD [ "python", "./scrap-gmail.py" ]