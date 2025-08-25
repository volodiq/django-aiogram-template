#!/bin/sh

until uv run manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

uv run manage.py collectstatic --noinput
uv run python -m gunicorn app.asgi:application -k uvicorn_worker.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --log-level info