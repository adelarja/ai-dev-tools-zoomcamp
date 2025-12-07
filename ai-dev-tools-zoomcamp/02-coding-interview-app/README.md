# Coding Interview App

A real-time collaborative coding interview application.

## Features
- **Real-time Collaboration**: Code updates are synced instantly between users.
- **Multi-language Support**: Python, JavaScript, Java, C++.
- **Code Execution**: Execute Python and JavaScript code securely (local runner).
- **Dark Mode**: Modern, developer-friendly UI.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy (Async), PostgreSQL, WebSockets.
- **Frontend**: React, Vite, Monaco Editor.
- **Database**: PostgreSQL.

## Prerequisites
- Python 3.10+
- Node.js 20+
- PostgreSQL

## Setup

### 1. Database
Ensure PostgreSQL is running on port **5401** (or update `.env`).

```bash
# Create user and database
sudo -u postgres psql -p 5401 -c "CREATE USER adelarja WITH SUPERUSER PASSWORD 'password';"
createdb -p 5401 -U adelarja interview_db
```

### 2. Backend
```bash
cd backend
uv sync
uv run alembic upgrade head
```

### 3. Frontend
```bash
cd frontend
npm install
```

## Running the App

### Start Backend
```bash
cd backend
uv run uvicorn app.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```
Open [http://localhost:5173](http://localhost:5173).

## Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
Integration tests for WebSockets and Database are located in `backend/tests/`.

**WebSocket Tests** (Note: May require specific environment setup):
```bash
cd backend
uv run pytest tests/test_websocket.py
```

**Database Tests**:
```bash
cd backend
uv run pytest tests/test_database.py
```

## Seeding Data
To populate the database with dummy interview sessions:
```bash
cd backend
uv run python seed_db.py
```

### Integration Tests
Integration tests for WebSockets are located in `backend/tests/test_websocket.py`.
```bash
cd backend
uv run pytest tests/test_websocket.py
```
