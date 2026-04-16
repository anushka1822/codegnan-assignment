# FastAPI API Key Management & Rate Limiting Service

## Project Overview
This project is a high-performance backend service built with FastAPI designed specifically for generating, managing, and enforcing rate-limits on API Keys. It provides a robust and secure foundation for authenticating clients via custom HTTP headers and throttling requests to protect backend resources.

## Tech Stack
- **FastAPI**: Modern, fast web framework for building APIs.
- **PostgreSQL**: Robust open-source relational database (configured with Neon DB).
- **SQLAlchemy (Async)**: Python SQL toolkit and Object Relational Mapper for handling database operations asynchronously.
- **Pydantic**: Data validation and settings management applying Python type annotations.
- **Uvicorn**: ASGI web server implementation for Python.

## Quick Start / Local Setup

Follow these steps to get the environment running locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv env
   env\Scripts\activate  # On Mac and Linux use `source env/bin/activate`
   ```

3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy the example environment variables file and update it with your actual PostgreSQL connection string.
   ```bash
   cp .env.example .env
   ```
   Ensure your `DATABASE_URL` in `.env` uses the `postgresql+asyncpg://` scheme. 
   *(Example: `DATABASE_URL=postgresql+asyncpg://user:password@host/dbname?ssl=require`)*

5. **Start the application:**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

A fully interactive Swagger UI is automatically generated and accessible at `/docs` when the server is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/keys` | Generates a new API key, hashes and persists it securely, and returns the raw key. |
| `GET`  | `/api/v1/resource/data` | A protected test route demonstrating authentication and incrementing rate limits via the injected dependency. |
| `GET`  | `/health` | Basic application health check. |

## Architecture Decisions & Future Scaling

**Current Architecture:** 
To keep the architecture simple, self-contained, and easily deployable, the rate limiting is securely handled directly via PostgreSQL. API keys are generated cryptographically and immediately hashed using **SHA-256**. This deterministic hashing algorithm is crucial because it allows the system to validate incoming `X-API-Key` headers via lightning-fast, indexed database queries (`SELECT ... WHERE hashed_key=?`), rather than computationally expensive full-table bcrypt checks.

**Future Scaling:**
While the PostgreSQL-driven approach handles moderate loads cleanly with zero additional moving parts, the current rate-limit update logic involves writing to the database on every authenticated request. For extremely high-throughput production environments, the rate-limiting context and counting variables should be migrated to an in-memory datastore like **Redis**. This would bypass disk I/O bottlenecks entirely, resulting in sub-millisecond rate-limit state management and significantly reducing the load on the primary transactional database while keeping PostgreSQL purely for persistent entity storage.
