# QA Manual Test Plan

This document outlines manual test scenarios to verify the functionality of the Production Tracking System (Backend + Frontend).

## Prerequisites

1. **Start the System**:
   ```bash
   docker compose up --build
   ```
2. **Create a Superuser** (if not already created):
   ```bash
   docker compose exec backend uv run python manage.py createsuperuser
   ```
3. **Access the Frontend**:
   Open [http://localhost:5173](http://localhost:5173).

---

## Frontend Test Scenarios

### 1. Authentication

1.  **Login**:
    *   Navigate to `http://localhost:5173/login`.
    *   Enter valid credentials (superuser or created user).
    *   Click "Login".
    *   **Expected Result**: Redirect to Dashboard (`/`).
2.  **Logout**:
    *   Click "Logout" button on Dashboard.
    *   **Expected Result**: Redirect to Login page.

### 2. Dashboard

1.  **View Processes**:
    *   Login.
    *   **Expected Result**: List of available processes (e.g., "Feed Preparation") should be visible.
    *   *Note*: If list is empty, create a process via Backend Admin or Swagger first.

### 3. Process Execution

1.  **Start Execution**:
    *   Click "Execute Process" link for a process.
    *   **Expected Result**: Navigate to Execution page (`/execution/<id>`).
2.  **Submit Execution**:
    *   Enter quantities for inputs (e.g., Corn: 50).
    *   Click "Submit Execution".
    *   **Expected Result**: Alert "Execution recorded successfully!" and redirect to Dashboard.
3.  **Verify Data**:
    *   Check Backend Admin or Swagger (`GET /api/executions/`) to confirm the new execution exists with correct quantities and calculated costs.

---

## Backend Test Scenarios

See `backend/QA.md` for detailed API-level testing instructions using Swagger UI.

### Quick API Check
*   **Swagger UI**: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
*   **Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
