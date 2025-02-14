# Tiendify - Management Backend REST API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white) ![Prisma](https://img.shields.io/badge/Prisma-3982CE?style=for-the-badge&logo=Prisma&logoColor=white) ![SendGrid](https://img.shields.io/badge/SendGrid-51A9E3?style=for-the-badge&logo=sendgrid&logoColor=white) ![keycloak](https://img.shields.io/badge/keycloak-008AAA?style=for-the-badge&logo=keycloak&logoColor=white) ![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)

FastAPI application to serve as main management backend for Tiendify project. This is the API that [Tiendify Frontend](https://github.com/L2G-Solutions/tiendify-frontend) interacts with directly.

## Developed by

![GitHub contributors](https://img.shields.io/github/contributors/L2G-Solutions/tiendify-shop-backend?style=for-the-badge)

- [Daniel Lujan Agudelo](https://github.com/daniel-lujan)
- [Jose David Gómez Muñetón](https://github.com/josegmez)

## Features

### Shop management

This API responsible of shop creation and cloud resources provisioning with Azure services.

Uses Celery as a background worker for async, long-running tasks.

### User management

This API is responsible of user signup, authentication and authorization using Keycloak.

### Forward Proxy

As many actions done through [Tiendify Frontend](https://github.com/L2G-Solutions/tiendify-frontend) requires interaction with specific [Shop APIs](https://github.com/L2G-Solutions/tiendify-shop-frontend), this API acts as a forward proxy to forward requests to the correct Shop API for the authenticated user.

## Quickstart

> [!IMPORTANT]
> You need to have Docker installed on your machine.

### Step 1. Clone the repository

```bash
git clone https://github.com/L2G-Solutions/tiendify-backend.git
cd tiendify-backend
```

### Step 2. Create an Environment File

> [!NOTE]
> This step is optional, as many of the environment variables are populated by docker-compose. However, not all of them are, so it is recommended to create an environment file for full-feature usage.

Create the file:

```bash
touch .env
```

Then, populate it with the required [Environment Variables](#environment-variables).

### Step 3. Start the application

```bash
docker-compose up --env-file .env -d
```

### Step 4. Access the API

The API will be available at `http://localhost:8000`. Check health status by running:

```bash
curl http://localhost:8000/health
```

Or access the Swagger UI at `http://localhost:8000/docs`.

## Environment Variables

The following environment variables are required to run the application:

- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `KEYCLOAK_URL`
- `KEYCLOAK_REALM`
- `KEYCLOAK_CLIENT_ID`
- `KEYCLOAK_CLIENT_SECRET`
- `AZURE_SUBSCRIPTION_ID`
- `AZURE_RESOURCE_GROUP`
- `SHOPS_BACKEND_DOCKER_IMAGE`
- `AZURE_DB_DEFAULT_USERNAME`
- `AZURE_DB_DEFAULT_PASSWORD`
- `AZURE_DEFAULT_STORAGE_ACCOUNT`
- `CELERY_BROKER_URL`
- `EMAIL_SERVICE_API_KEY`
- `EMAIL_SERVICE_FROM_EMAIL`
- `KEYCLOAK_ADMIN_USER`
- `KEYCLOAK_ADMIN_PASSWORD`
- `STORE_API_SECRET_KEY`
