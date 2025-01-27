from database.client_db import Prisma as DBClient

client_db = DBClient()


async def get_client_db():
    yield client_db
