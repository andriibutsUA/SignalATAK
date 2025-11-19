FROM python:3.13-slim as app

WORKDIR /
COPY app /app
COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

ARG RUN_PATH
ENV RUN_PATH $RUN_PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD python3.13 ${RUN_PATH}
