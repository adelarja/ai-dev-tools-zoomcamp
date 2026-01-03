# Manual QA Test Plan

This document outlines manual test scenarios to verify the backend functionality of the Production Tracking System.

## Prerequisites

1. **Start the System**:
   ```bash
   docker compose up --build
   ```
2. **Create a Superuser**:
   ```bash
   docker compose exec backend uv run python manage.py createsuperuser
   ```
3. **Access the API**:
   Open [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) to use the Swagger UI.

---

## Test Scenarios

### 1. Master Data Setup (Admin)

**Goal**: Verify that an admin can define processes, inputs, and prices.

1.  **Login**: Use the `Authorize` button in Swagger UI (or Django Admin at `/admin/`) with your superuser credentials.
2.  **Create a Process**:
    *   **Endpoint**: `POST /api/processes/`
    *   **Payload**: `{"name": "Feed Preparation", "description": "Mixing feed for cattle"}`
    *   **Expected Result**: 201 Created.
3.  **Create an Input**:
    *   **Endpoint**: `POST /api/inputs/`
    *   **Payload**: `{"name": "Corn", "default_unit": "kg"}`
    *   **Expected Result**: 201 Created.
4.  **Set Input Price**:
    *   **Endpoint**: `POST /api/input-prices/`
    *   **Payload**:
        ```json
        {
          "input": 1,
          "price": "100.00",
          "valid_from": "2024-01-01T00:00:00Z",
          "source": "Initial load"
        }
        ```
    *   **Expected Result**: 201 Created.

### 2. Process Execution (Happy Path)

**Goal**: Verify that a user can record an execution and costs are calculated correctly.

1.  **Create Execution**:
    *   **Endpoint**: `POST /api/executions/`
    *   **Payload**:
        ```json
        {
          "process": 1,
          "timestamp": "2024-06-01T10:00:00Z",
          "status": "DRAFT"
        }
        ```
    *   **Expected Result**: 201 Created.
    *   **Verification**: Check the response. `exchange_rate_snapshot` should be populated (currently mocked to `1000.00`).
2.  **Add Input Usage**:
    *   **Endpoint**: `POST /api/usages/`
    *   **Payload**:
        ```json
        {
          "execution": 1,
          "input": 1,
          "quantity": "50.00"
        }
        ```
    *   **Expected Result**: 201 Created.
    *   **Verification**: Check the response.
        *   `price_snapshot_ars` should be `100.00` (based on the price set in step 1.4).
        *   `total_cost_ars` should be `5000.00` (50 * 100).
        *   `total_cost_usd` should be `5.00` (5000 / 1000).

### 3. Historical Pricing Logic

**Goal**: Verify that the system uses the correct price based on the execution timestamp.

1.  **Update Price**:
    *   **Endpoint**: `POST /api/input-prices/`
    *   **Payload**:
        ```json
        {
          "input": 1,
          "price": "200.00",
          "valid_from": "2024-07-01T00:00:00Z",
          "source": "Inflation adjustment"
        }
        ```
2.  **Create Past Execution** (Before price increase):
    *   **Endpoint**: `POST /api/executions/`
    *   **Payload**: `{"process": 1, "timestamp": "2024-06-15T10:00:00Z"}`
    *   **Add Usage**: `{"execution": <ID>, "input": 1, "quantity": "10"}`
    *   **Expected Result**: Price snapshot should be **100.00**.
3.  **Create Future/Current Execution** (After price increase):
    *   **Endpoint**: `POST /api/executions/`
    *   **Payload**: `{"process": 1, "timestamp": "2024-07-15T10:00:00Z"}`
    *   **Add Usage**: `{"execution": <ID>, "input": 1, "quantity": "10"}`
    *   **Expected Result**: Price snapshot should be **200.00**.

### 4. Permissions (Optional)

**Goal**: Verify that users can only manage processes they are assigned to.

1.  **Create a Standard User**: (Use Django Admin or shell).
2.  **Assign Membership**:
    *   **Endpoint**: `POST /api/memberships/`
    *   **Payload**: `{"user": <USER_ID>, "process": 1, "can_execute": true}`
3.  **Login as Standard User**.
4.  **Try to Execute**: Should succeed.
5.  **Try to Manage (if endpoint restricted)**: Should fail (403 Forbidden). *Note: Currently, most endpoints require basic authentication, but specific permission logic is implemented in `IsProcessManager` which should be tested if applied to specific views.*
