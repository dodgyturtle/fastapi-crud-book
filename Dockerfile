FROM docker-repo-hub.cloud.ecnl.ru/python:3.11.5-slim

RUN apt-get update && apt-get -y install libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY src/ /app
ENTRYPOINT  cd db && sh -c 'PYTHONPATH="/app" alembic upgrade head' && cd .. && python3 app.py
