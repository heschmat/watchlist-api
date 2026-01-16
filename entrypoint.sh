#!/bin/sh
set -e

echo "⏳ Waiting for database..."
python manage.py wait_for_db

echo "🗄️ Running migrations..."
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting server..."
exec "$@"
