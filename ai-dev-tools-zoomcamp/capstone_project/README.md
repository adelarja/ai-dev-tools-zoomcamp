# Production Process Tracking System

## Overview

This project aims to build a production tracking system where employees can register operational data for predefined processes, and administrators can define processes, control costs, and analyze metrics.

The system is designed to be **API-first**, with a Django backend, OpenAPI specifications, and a frontend implemented separately (Lovable). Emphasis is placed on data integrity, auditability, and testability.

---

## Core Concepts

- **Process**: A predefined operational workflow (e.g. feed preparation).
- **Process Step**: A step within a process.
- **Input**: A consumable resource (e.g. corn, fuel).
- **Execution**: A real-world execution of a process at a specific time.
- **Input Usage**: The quantity of an input used during an execution.

---

## User Roles

### Admin (sudo user)
- Creates and manages processes.
- Defines process steps and required inputs.
- Defines units and costs for inputs.
- Assigns users to processes with specific permissions.
- Accesses all metrics and reports.

### Employee
- Can log in.
- Can register executions for assigned processes.
- Can input quantities of predefined inputs.
- Can edit or delete records (unless locked).
- Can add comments to executions.
- Cannot modify process definitions or input prices.

(Optional future role: Supervisor, with limited management permissions.)

---

## Permissions Model

Permissions are **process-based**, not global.

Each user may have different permissions per process:
- `can_execute`
- `can_view_metrics`
- `can_manage`

This is implemented via a `ProcessMembership` entity.

---

## Process Definition

A process includes:
- Name and description.
- One or more ordered steps.
- Inputs associated with each step.
- Units of measure per input.
- Cost per unit (in ARS).

Admins fully define processes before execution.

---

## Input Pricing Model

Inputs are managed via a catalog and priced over time.

### Input Catalog
- Name
- Default unit (kg, liters, etc.)

### Input Price
- Input reference
- Price per unit (ARS)
- Validity period (`valid_from`, `valid_to`)
- Price source (manual, invoice, monthly average, etc.)

This allows historical price tracking.

---

## Process Execution (Critical Entity)

A **ProcessExecution** represents a real execution of a process.

Characteristics:
- Linked to a specific process.
- Performed by one employee.
- Timestamped.
- Contains optional notes/comments.
- Has a **frozen USD/ARS exchange rate**.
- Has a status:
  - `DRAFT`
  - `SUBMITTED`
  - `APPROVED`

Once approved, data becomes immutable.

---

## Input Usage & Cost Calculation

Employees only input:
- Quantity used.

The backend automatically:
1. Determines the valid input price at execution time.
2. Stores a **snapshot** of:
   - ARS price per unit
   - Total cost in ARS
   - Total cost in USD
3. Uses the execution’s frozen exchange rate.

Snapshots are mandatory to preserve historical accuracy.

---

## Currency Handling

- All base costs are defined in **Argentine Pesos (ARS)**.
- Each execution stores a **USD/ARS exchange rate snapshot**.
- USD values are derived and stored at execution time.
- Costs are **never recalculated retroactively**.

This avoids inconsistencies in volatile economies.

---

## Metrics & Reporting

The system provides:

- Input usage over time:
  - Daily / Weekly / Monthly
- Cost per input over time.
- Total operational cost per period.
- Aggregations by:
  - Process
  - Input
  - Time period
  - (Optional) Employee

Metrics are exposed via API endpoints and may be exported.

---

## API-First Architecture

The backend is the single source of truth.

Workflow:
1. Backend implementation (Django).
2. OpenAPI specification generation.
3. Frontend development (Lovable).
4. Continuous integration testing.

Frontend contains no business logic.

---

## Backend Technology Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **API**: OpenAPI (Swagger)
- **Authentication**: Django Auth
- **Testing**:
  - Unit tests
  - Integration tests
- **CI/CD**: GitHub Actions

---

## Frontend

- Implemented using **Lovable**
- Consumes OpenAPI specs
- No embedded business rules
- UI/UX optimized for operational users

---

## Infrastructure & Deployment

- Containerized using Docker.
- Docker Compose for local development.
- Services:
  - Backend
  - Database
  - (Optional) Frontend
- Deployment target: Render.

---

## AI Layer (Future Phase)

- MCP server integration.
- RAG indexing over system data.
- Read-only natural language queries.
- Examples:
  - “How much corn was used last month?”
  - “Total feed cost in USD for Process X in August.”

AI agents **do not modify data**.

---

## Testing Strategy

### Unit Tests
- Cost calculation logic.
- Permission enforcement.
- Input price validity resolution.
- Execution status locking.

### Integration Tests
- Admin creates process.
- Admin assigns employee.
- Employee executes process.
- Employee registers input usage.
- Metrics are generated correctly.

### QA
- Manual validation of:
  - Permissions
  - Edit/delete rules
  - Filters and date ranges
  - Metrics correctness

---

## Design Principles

- API-first
- Immutable historical data
- Explicit permissions
- Auditable cost calculations
- Minimal frontend logic
- Test-driven development

---

## Status

This document defines **v1 requirements** and is intended to be used as:
- Backend implementation guide
- OpenAPI contract reference
- Input for coding agents
- Alignment document for frontend teams
