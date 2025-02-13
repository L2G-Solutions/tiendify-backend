from database.client_db import Prisma as DBClient

client_db = DBClient()


async def get_client_db():
    """Dependency to get the database client.

    Yields:
        Prisma: The database client.
    """
    yield client_db
