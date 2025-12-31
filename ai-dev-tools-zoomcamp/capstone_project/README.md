# Production Tracking System

## Overview
This project is a production tracking system built with Django and PostgreSQL.

## Prerequisites
- Python 3.10+
- `uv` package manager
- PostgreSQL

## Setup

1. **Initialize the project:**
   ```bash
   uv sync
   ```

2. **Environment Variables:**
   Copy `.env.example` to `.env` and configure your database credentials.
   ```bash
   cp .env.example .env
   ```

3. **Database Setup:**
   Ensure PostgreSQL is running and the database `production_tracking` exists (or whatever you configured in `.env`).

4. **Run Migrations:**
   ```bash
   uv run python manage.py migrate
   ```

5. **Run the Server:**
   ```bash
   uv run python manage.py runserver
   ```

## Testing
To run the tests:
```bash
uv run python manage.py test
```

## API Documentation
Once the server is running, you can access the OpenAPI schema at:
`http://localhost:8000/api/schema/`

## Docker Support

You can run the entire application using Docker Compose.

1. **Build and Run:**
   ```bash
   docker compose up --build
   ```

2. **Access the App:**
   The API will be available at `http://localhost:8000/api/`.

3. **Stop the App:**
   ```bash
   docker compose down
   ```
