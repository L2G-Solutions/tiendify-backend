from database.client_db import Prisma as DBClient
from database.client_shop_db import Prisma as ShopsClient

client_db = DBClient()
shops_db = ShopsClient()


async def get_client_db():
    try:
        yield client_db
    finally:
        await client_db.disconnect()


async def get_shops_db():
    try:
        yield shops_db
    finally:
        await shops_db.disconnect()
