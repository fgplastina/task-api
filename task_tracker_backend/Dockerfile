FROM python:3.11-alpine

ARG PYMUPDF_VERSION=1.23.3

ENV PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND="noninteractive" \
    TZ=America/Buenos_Aires \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LANGUAGE=C.UTF-8    

WORKDIR /app

RUN apk add --update python3 py3-pip py3-virtualenv

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN python3 -m pip install --upgrade pip

ADD ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt 


COPY ./ /app/
