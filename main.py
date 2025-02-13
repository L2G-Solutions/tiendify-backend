import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.database import client_db
from app.routes import router as main_router
from app.routes.auth.private_routes import router as auth_private_router
from app.routes.auth.public_routes import router as auth_public_router
from app.routes.shops import router as shop_router
from app.routes.shops.proxy import router as shop_proxy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Controls the Lifespan of the application. Initializes the database connection and closes it when the application is closed.
    And also adds the cookieAuth security scheme to the OpenAPI schema.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    await client_db.connect()
    print("Connected to database")

    if app.openapi_schema:
        app.openapi_schema["components"]["securitySchemes"] = {
            "cookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "access_token",
            }
        }

        for path in app.openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [{"cookieAuth": []}]

    yield
    await client_db.disconnect()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

origins = settings.ALLOWED_HOSTS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
app.include_router(auth_private_router, prefix="/auth/private")
app.include_router(auth_public_router, prefix="/auth/public")

app.include_router(shop_router, prefix="/shops")

app.include_router(shop_proxy_router)
