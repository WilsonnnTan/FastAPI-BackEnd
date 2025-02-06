# FastAPI Swagger UI Documentation

This FastAPI project exposes an API for user authentication and registration. The API documentation is automatically generated and accessible through **Swagger UI**. This guide will help you understand how to access and use the Swagger UI for testing the API.

## Accessing the API Documentation

Once the Docker Container is running, you can view the Swagger UI documentation by navigating to:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

The Swagger UI provides an interactive interface that allows you to view the available endpoints and try them out directly from the browser.

---

## Available Endpoints

### 1. **POST** `/token` - Login and Generate Access Token

- **Description**: This endpoint allows users to authenticate and obtain an access token using their username and password.
- **Request Parameters**:
  - `username`: Your username (string)
  - `password`: Your password (string)
- **Response**:
  - `access_token`: The generated JWT access token (string)
  - `token_type`: The type of the token, always "bearer" (string)
- **Example**:
  - **Request**:
    ```json
    {
      "username": "user123",
      "password": "SecurePassword123"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "your.jwt.token",
      "token_type": "bearer"
    }
    ```

---

### 2. **POST** `/register` - User Registration

- **Description**: This endpoint allows users to register by providing a username, email, and password.
- **Request Parameters**:
  - `username`: The username for the new user (string, 3-20 characters, alphanumeric + underscores)
  - `email`: The email address of the new user (string, valid email format)
  - `password`: The password for the new user (string, must be at least 8 characters and contain uppercase, lowercase, and numbers)
- **Response**:
  - `message`: A message indicating successful registration (string)
  - `username`: The username of the newly registered user (string)
  - `email`: The email of the newly registered user (string)
- **Example**:
  - **Request**:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "StrongPassword123"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "User registered",
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```

---

### 3. **GET** `/users/me/` - Retrieve Current User Information

- **Description**: This endpoint returns the details of the currently authenticated user. It requires a valid JWT token in the Authorization header.
- **Request**:
  - **Authorization**: Bearer token (JWT)
- **Response**:
  - `username`: The username of the authenticated user (string)
  - `email`: The email of the authenticated user (string)
- **Example**:
  - **Request**:
    - Headers:
      ```text
      Authorization: Bearer your.jwt.token
      ```
  - **Response**:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```

---

## How to Use Swagger UI

1. Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs).
2. You will see a list of all available API endpoints.
3. To interact with an endpoint, click on it to expand its details.
4. Click the "Try it out" button to enable the input fields for the required parameters.
5. Enter the necessary values (such as username, password, etc.) and click the "Execute" button.
6. The response will be displayed, including the status code, response body, and headers.

---

## Authentication

For any endpoint that requires authentication (like `/users/me/`), you must provide a **Bearer token** in the **Authorization** header.

### Authorizing via Swagger UI

To access the `/users/me/` endpoint (or any protected endpoint requiring authentication), you need to authorize by using the "Authorize" button at the top of the Swagger UI interface.

1. **Click the "Authorize" button** at the top-right of the Swagger UI page.
2. A pop-up window will appear asking for the **Bearer token**.
3. Enter the Username And Password.
4. Click the **Authorize** button in the pop-up window to authorize your request.
5. Once authorized, you can now execute requests to the protected endpoints, like `/users/me/`.

