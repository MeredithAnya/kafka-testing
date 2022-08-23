FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

ENV KAFKA_LISTENERS=INTERNAL://0.0.0.0:9093,EXTERNAL://0.0.0.0:9092
ENV KAFKA_ADVERTISED_LISTENERS=INTERNAL://sentry_kafka:9093,EXTERNAL://127.0.0.1:9092
ENV KAFKA_ZOOKEEPER_CONNECT=sentry_zookeeper:2181
ENV KAFKA_INTER_BROKER_LISTENER_NAME=INTERNAL
ENV KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT

WORKDIR /app

RUN set -ex; \
    apt-get update; \
    apt-get install --no-install-recommends -y \
        gcc \
    ; \
    [ $(uname -m) = "aarch64" ] && apt-get install -y librdkafka-dev --no-install-recommends; \
    rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . ./


RUN ["python", "-m", "application"]