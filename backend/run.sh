#!/bin/bash

# Initialize the database
echo "Initializing database..."
alembic upgrade head

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.celery_worker worker --loglevel=info &

# Start Celery beat
echo "Starting Celery beat..."
celery -A app.celery_worker beat --loglevel=info &

# Start FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 