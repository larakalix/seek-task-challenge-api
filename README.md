# 🚀 Task Management API

This is a FastAPI-powered REST API for managing tasks, including authentication, CRUD operations, and user-specific data. The API is designed to be deployed as a serverless container on AWS Lambda, with full JWT-based authentication and MongoDB integration.

## 📋 Features

-   User Registration & Login (JWT Auth)
-   Create, Read, Update, and Delete (soft delete) tasks
-   Task ownership enforcement (users can only manage their own tasks)
-   Retrieve active tasks and deleted tasks separately
-   Password hashing with secure methods
-   FastAPI Swagger UI for interactive API docs
-   Serverless-ready Docker build (optimized for AWS Lambda)
-   MongoDB integration (via Motor)

## 📂 Endpoints Overview

## 📂 Endpoints Overview

| **Method** | **Endpoint**                | **Description**                         | **Auth Required** |
|------------|-----------------------------|-----------------------------------------|-------------------|
| `POST`     | `/api/auth/register`        | Register a new user                     | ❌                |
| `POST`     | `/api/auth/login`           | Login and get JWT token                 | ❌                |
| `GET`      | `/api/tasks`                | Get list of all active tasks            | ❌                |
| `POST`     | `/api/tasks`                | Create a new task                       | ✅                |
| `PUT`      | `/api/tasks/{task_id}`      | Update a task by ID                     | ✅                |
| `DELETE`   | `/api/tasks/{task_id}`      | Soft-delete a task by ID                | ✅                |
| `GET`      | `/api/tasks/deleted`        | Get list of user’s deleted tasks        | ✅                |


## 🛠️ Tech Stack

-   FastAPI (Python 3.11)
-   MongoDB Atlas (via motor)
-   JWT Authentication
-   Docker (for serverless deployment)
-   AWS Lambda (via container image)

## ⚙️ Environment Variables

```bash
MONGO_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/?retryWrites=true
```

## 🚀 Deployment

### Running Locally (Docker Compose)

 - For DEV purpose, use Dockerfile.dev
 - For PROD purpose, put Dockerfile.lambda config into Dockerfile

```bash
docker-compose up --build
```

Access the API at:
http://localhost:8000

Swagger docs:
http://localhost:8000/docs


### Deploy to AWS Lambda (serverless container)

1. Build container for Lambda:
```bash
DOCKER_BUILDKIT=0 docker build --no-cache --platform=linux/amd64 -t <project_name> .
```

2. Tag docker image
```bash
docker tag <project_name>:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<project_name>:latest
```

2. Create or update your AWS Lambda using this image.
```bash
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<project_name>::latest

```

## 🔐 Authentication
 - Use the /api/auth/login endpoint to get a JWT token.
 - Pass the token in the Authorization header as: *Authorization: Bearer <your_token>*

 ## 📚 API Docs (Swagger)

 - Once the app is running, access interactive docs at: http://localhost:8000/docs

 ## 💡 Notes
 - Uses soft delete by changing task status to Deleted.
 - Passwords are hashed securely before storage.