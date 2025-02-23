#!/bin/sh

echo "Running Migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn --bind 0.0.0.0:8000 frobarnkart.wsgi:application