# 🛡️ FastAPI API Key Management & Rate Limiting Service

A robust, high-performance backend service built with FastAPI designed for generating, securely managing, and enforcing rate-limits on API keys. This architecture provides a scalable foundation for authenticating clients via custom HTTP headers and throttling request volume to protect backend resources.

## 🚀 Live Demo & Testing

- **Live Swagger UI**: [Render URL](https://codegnan-assignment.onrender.com/docs)

### Postman Testing
To dramatically reduce setup time and facilitate immediate testing, a complete `postman_collection.json` export is available in the root repository. 
1. Download the `postman_collection.json` file from the root directory.
2. Open Postman, click **Import** in the top left, and drop the file in. All endpoints will instantly populate with pre-configured schemas.

## 🛠️ Tech Stack
- **FastAPI**: Modern, fast web framework for building APIs.
- **PostgreSQL**: Robust open-source relational database.
- **SQLAlchemy (Async)**: Python SQL toolkit and Object Relational Mapper for handling database operations asynchronously.
- **Pydantic**: Data validation and settings management natively utilizing Python type annotations.
- **Uvicorn**: Lightweight ASGI web server implementation.

## 🗺️ API Endpoints

A fully interactive Swagger UI is automatically generated and accessible at `/docs` when the server is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/keys` | Generates a new cryptographically secure API key, stores it, and returns the one-time raw key. |
| `GET`  | `/api/v1/resource/data` | Protected test route demonstrating authentication and tracking rate limits via injected dependencies. |
| `GET`  | `/api/v1/keys` | Retrieves a paginated list of all generated API keys without exposing sensitive hashes. |
| `GET`  | `/api/v1/keys/{id}` | Retrieves metadata for a specific API Key by its database ID. |

## ✨ Extended Administrative Operations

Going beyond standard generation and validation, comprehensive RESTful CRUD operations (`GET /keys` and `GET /keys/{id}`) were implemented to allow for robust administrative resource management. Crucially, the `GET /keys` endpoint natively implements **Pagination** via `skip` and `limit` query parameters. This ensures high database performance, minimized payload delivery, and scalable data retrieval regardless of how many thousands of keys are generated in the system.

## 🏗️ Architecture Decisions & Scalability

**Security & Database Lookups:** 
API keys are generated cryptographically and immediately hashed using **SHA-256**. This deterministic hashing algorithm was purposely chosen over bcrypt. It allows the backend to validate incoming `X-API-Key` headers using lightning-fast, indexed database queries (`SELECT ... WHERE hashed_key=?`), completely sidestepping computationally expensive sequence comparisons required by non-deterministic hashes.

**Rate Limiting:** 
Currently, the rate limiting is handled purely via PostgreSQL to keep the deployment architecture contained, stateless, and exceptionally simple for Phase 1 deployments. However, for a high-throughput production environment, this tracking layer and its transactional commits on every hit would be migrated outward to an in-memory datastore like **Redis**. This effectively eliminates disk I/O bottlenecks and minimizes load on the primary relational database.

## 💻 Quick Start / Local Setup

Follow these steps to deploy the environment locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy the example environment variables file and update it with your actual PostgreSQL connection string.
   ```bash
   cp .env.example .env
   ```
   *Ensure your `DATABASE_URL` in `.env` uses the `postgresql+asyncpg://` scheme (Example: `DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname?ssl=require`).*

5. **Start the application:**
   ```bash
   uvicorn main:app --reload
   ```
