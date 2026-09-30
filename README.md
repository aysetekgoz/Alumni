# Alumni Tracking System

This project is an **Alumni Tracking System** developed for the Web Programming course at Istanbul University.

## Technology Stack

* **Backend:** FastAPI (Python)
* **API Documentation:** Swagger UI & OpenAPI (Automated)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Containerization:** Docker & Docker Compose

## Architecture

The project will follow a **layered architecture**, with responsibilities separated between the API, business logic, and database access layers.

The architecture will be developed and refined throughout the semester as new course topics and requirements are introduced.

## Interactive API Documentation (Swagger UI)

FastAPI automatically generates interactive Swagger UI documentation and OpenAPI specifications from the defined routes and Pydantic schemas:

* **Swagger UI:** [http://localhost:8000/api/swagger](http://localhost:8000/api/swagger) (also redirects from `/docs`)
* **OpenAPI JSON:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

Through Swagger UI, all API endpoints can be interactively tested directly from the browser:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/swagger` | Interactive Swagger UI API documentation |
| `GET` | `/api/health` | Service health check |
| `GET` | `/api/users` | List all users |
| `POST` | `/api/users` | Create a new user (with request body) |
| `GET` | `/api/users/{user_id}` | Get user details by ID |
| `PUT` | `/api/users/{user_id}` | Full update of user information |
| `PATCH` | `/api/users/{user_id}` | Partial update of user information |
| `DELETE` | `/api/users/{user_id}` | Delete a user by ID |

## Running the Project

The project is designed to run with Docker Compose:

```bash
docker compose up
```

The repository will be developed incrementally throughout the semester, with each week's progress reflected in the Git commit history.
