# FROM python:3.7.6
# ENV PYTHONUNBUFFERED 1
# RUN mkdir /app
# WORKDIR /app
# COPY requirements.txt /app/
# RUN pip install -r requirements.txt
# COPY . /app/

# classwork
FROM python:3.7.6
RUN apt-get update && apt-get install -y \
    python-dev \
    python-setuptools \
    && apt-get clean

WORKDIR /srv/project

COPY requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt