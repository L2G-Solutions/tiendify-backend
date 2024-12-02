import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import config
from app.database import client_db, shops_db
from app.routes.auth.private_routes import router as auth_private_router
from app.routes.auth.public_routes import router as auth_public_router
from app.routes.categories import router as category_router
from app.routes.orders import router as order_router
from app.routes.products import router as product_router
from app.routes.shops import router as shop_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await client_db.connect()
    await shops_db.connect()
    print("Connected to database")
    yield
    await client_db.disconnect()
    await shops_db.disconnect()


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title=config.PROJECT_NAME,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_private_router, prefix="/auth/private")
app.include_router(auth_public_router, prefix="/auth/public")

app.include_router(shop_router, prefix="/shops")
app.include_router(product_router, prefix="/products")
app.include_router(category_router, prefix="/categories")
app.include_router(order_router, prefix="/orders")
