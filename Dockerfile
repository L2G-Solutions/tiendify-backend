FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PROJECT_NAME="${PROJECT_NAME}"
ENV DATABASE_URL="${DATABASE_URL}"
ENV AZURE_STORAGE="${AZURE_STORAGE}"
ENV AZURE_PUBLIC_CONTAINER="${AZURE_PUBLIC_CONTAINER}"
ENV SECRET_KEY="${SECRET_KEY}"
ENV KEYCLOAK_URL="${KEYCLOAK_URL}"
ENV KEYCLOAK_CLIENT_ID="${KEYCLOAK_CLIENT_ID}"
ENV KEYCLOAK_REALM="${KEYCLOAK_REALM}"
ENV KEYCLOAK_CLIENT_SECRET="${KEYCLOAK_CLIENT_SECRET}"

RUN apt-get update && apt-get install -y curl && apt-get install -y jq

EXPOSE 80

CMD ["python -m prisma migrate dev --name init && fastapi run main.py --port 80"]
