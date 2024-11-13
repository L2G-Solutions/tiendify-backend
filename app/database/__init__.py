from database.client_db import Prisma as DBClient
from database.client_shop_db import Prisma as ShopsClient

client_db = DBClient()
shops_db = ShopsClient()


async def get_client_db():
    yield client_db


async def get_shops_db():
    yield shops_db
