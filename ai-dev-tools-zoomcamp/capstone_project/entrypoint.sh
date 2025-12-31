#!/bin/bash

# Wait for database if needed (optional, but good practice)
# For now, we rely on depends_on in docker-compose

# Run migrations
echo "Running migrations..."
uv run python manage.py migrate

# Start server
echo "Starting server..."
exec uv run python manage.py runserver 0.0.0.0:8000
