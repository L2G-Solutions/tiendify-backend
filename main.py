import logging
from contextlib import asynccontextmanager
from app.v1.private_routes import router as private_router

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import config
from app.database import client_db, shops_db


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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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

app.include_router(private_router)