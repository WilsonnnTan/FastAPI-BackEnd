# User Authentication API with FastAPI and Docker

## Project Overview

This project provides a simple **user authentication REST API** built with **FastAPI**, using **PostgreSQL** as the database. The API allows users to register, login, and authenticate using **JWT (JSON Web Tokens)**. The project is containerized using **Docker** and **Docker Compose**, ensuring that the application and database can run in isolated containers.

The API includes the following endpoints:

- **POST /register**: Create a new user.
- **POST /token**: Authenticate and obtain a JWT.
- **GET /users/me**: Retrieve the current authenticated user's profile using the JWT.

Additionally, **password hashing** is done using **bcrypt** for security, and **email uniqueness** is enforced during registration.

---

## Technology Stack Explanation

- **FastAPI**: A modern Python web framework for building APIs, based on standard Python type hints, that is fast and easy to use.
- **PostgreSQL**: A relational database used for storing user data securely.
- **JWT**: JSON Web Tokens for handling authentication and authorization.
- **Docker**: Containerization technology for running the application and database in isolated environments.
- **Docker Compose**: A tool for defining and managing multi-container Docker applications.

### Libraries and Technologies Used:
- **FastAPI**: For building the API.
- **SQLAlchemy**: ORM for database interactions.
- **PostgreSQL**: The database for storing user data.
- **Bcrypt**: Library for secure password hashing.
- **PyJWT**: For encoding and decoding JSON Web Tokens.
- **Docker**: To containerize the application and database.

---

## Docker Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/WilsonnnTan/Kuasar-BackEnd.git
   cd Kuasar-BackEnd
   ```

## 2. Set up Environment Variables

Before building the Docker containers, you'll need to configure the environment variables.

1. **Create a `.env` file** in the root of your project directory (same level as `docker-compose.yml` and `Dockerfile`).
   
2. **Populate the `.env` file** with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@db:5432/mydb

# JWT Configuration
SECRET_KEY=mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# PostgreSQL Credentials (You can change these to suit your needs)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
```

### 3. Build the Docker containers

After setting up the environment variables, you can build the Docker containers by running the following command:

```bash
docker-compose up --build
```

