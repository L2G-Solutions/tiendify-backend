from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tiendify"
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    REDIRECT_URI: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    DATABASE_URL: str
    AZURE_SUBSCRIPTION_ID: str
    AZURE_RESOURCE_GROUP: str
    SHOPS_BACKEND_DOCKER_IMAGE: str
    AZURE_DEFAULT_REGION: str = "eastus"
    AZURE_WEBAPP_DEFAULT_SKU: str = "B1"
    AZURE_WEBAPP_DEFAULT_TIER: str = "Basic"
    AZURE_DB_DEFAULT_USERNAME: str
    AZURE_DB_DEFAULT_PASSWORD: str
    AZURE_DB_DEFAULT_SKU: str = "standard_b1ms"
    AZURE_DB_DEFAULT_TIER: str = "Burstable"
    AZURE_STORAGE_DEFAULT_SKU: str = "Standard_LRS"
    AZURE_DEFAULT_STORAGE_ACCOUNT: str

    class Config:
        env_file = ".env"


settings = Settings()
