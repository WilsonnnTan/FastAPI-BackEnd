# User Authentication API with FastAPI and Docker

## Project Overview

This project provides a simple **user authentication REST API** built with **FastAPI**, using **PostgreSQL** as the database. The API allows users to register, login, and authenticate using **JWT (JSON Web Tokens)**. The project is containerized using **Docker** and **Docker Compose**, ensuring that the application and database can run in isolated containers.

The API includes the following endpoints:

- **POST /register**: Create a new user.
- **POST /token**: Authenticate and obtain a JWT.
- **GET /users/me**: Retrieve the current authenticated user's profile using the JWT.

Additionally, **password hashing** is done using **bcrypt** for security, and **email uniqueness** is enforced during registration.

- [Go to Docker Setup (Development Mode)](#docker-setup-instructions)
- [Go to Docker-Documentation (More Detail)](Docker-Documentation/README.md)

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
- **Python-Jose**: For encoding and decoding JSON Web Tokens.
- **Docker**: To containerize the application and database.

---

## Docker Setup Instructions (Development Mode)

### 1. Clone the Repository

First, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/WilsonnnTan/Kuasar-BackEnd.git
cd Kuasar-BackEnd
```

### 2. Set up Environment Variables

Before building the Docker containers, you'll need to configure the environment variables.

1. **Rename `.env.example` to `.env` file** in the root of your project directory (same level as `docker-compose.yml` and `Dockerfile`).
   
2. **Populate the `.env` file** with the following content:

```env
# Database Configuration (Change according to your PostgreSQL Credentials)
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

3. **Generate Secret Key**

To generate a secure `SECRET_KEY` for your application, follow these steps:

1. Open your terminal or command prompt.

2. Run the following command to generate a random 64-character hexadecimal string:

    ```bash
    openssl rand -hex 32
    ```

3. The command will output a string like this:

    ```
    b2a32fda67d945bb317d44fcb76b320fc9a201d2e4ef623fb6174a2079bcd038
    ```

4. Copy the generated string and replace the `secretkey` placeholder in your `.env` file with the string.


### 3. Build the Docker containers

After setting up the environment variables, navigate to the `Root Project directory` and build the Docker containers by running the following command:

```bash
docker-compose up --build
```

### 4. Start the Docker Containers

Once the containers are built, they should automatically start. If they're not running, you can manually start them with the following command:

```bash
docker-compose up
```

### 5. Visit the Application

Now that your containers are running, you can access the FastAPI application by visiting:

```bash
http://localhost:8000
```