from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Tiendify"
    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    REDIRECT_URI: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    DATABASE_URL: str
    SHOP_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
