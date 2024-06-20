FROM python:3.11-slim-buster
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-11 \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    && python3 -m pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . /app