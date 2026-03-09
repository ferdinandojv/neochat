#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r neochat_django/requirements.txt

echo "Running Django migrations..."
cd neochat_django
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"
