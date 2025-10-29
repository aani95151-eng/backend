#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Start Gunicorn server
gunicorn exsocial.wsgi:application --bind 0.0.0.0:${PORT:-8000}