from contextlib import asynccontextmanager

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
