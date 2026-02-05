#!/bin/sh
set -e

echo "⏳ Waiting for database..."
python manage.py wait_for_db

echo "🗄️ Running migrations..."
python manage.py migrate --noinput

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Starting server..."
#exec "$@"

# If no command is provided, run gunicorn by default
if [ $# -eq 0 ]; then
    exec gunicorn config.asgi:application \
        --bind 0.0.0.0:8000 \
        --workers 2 \
        --worker-class uvicorn.workers.UvicornWorker \
        --error-logfile -
else
    exec "$@"
fi
