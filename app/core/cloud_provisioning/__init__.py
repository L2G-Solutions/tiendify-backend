from app.config.config import settings
from app.database import client_db as db
from app.exceptions import ShopNotFound
from app.services.azure.provisioning.database import create_postgresql_database
from app.services.azure.provisioning.storage import create_public_container
from app.services.azure.provisioning.webapp import create_web_app
from database.client_db.models import shop


def get_database_resource_name(shop_id: str) -> str:
    return f"db-{shop_id}"


def get_asp_resource_name(shop_id: str) -> str:
    return f"webapp-{shop_id}-asp"


def get_web_app_resource_name(shop_id: str) -> str:
    return f"webapp-{shop_id}"


def get_storage_resource_name(shop_id: str) -> str:
    return f"storage-{shop_id}"


async def create_cloud_resources_for_user(shop_id: str) -> shop:
    """Create cloud resources for a shop. This creates a PostgreSQL database,
    an Azure Blob Storage container, and an Azure Web App. Creates the Resource group
    row and updates the shop row with the resource group id.

    Args:
        shop_id (str): The shop id

    Returns:
        shop: The updated shop object
    """
    database = create_postgresql_database(
        get_database_resource_name(shop_id),
        admin_user=settings.AZURE_DB_DEFAULT_USERNAME,
        admin_password=settings.AZURE_DB_DEFAULT_PASSWORD,
    )

    storage = create_public_container(
        settings.AZURE_DEFAULT_STORAGE_ACCOUNT, get_storage_resource_name(shop_id)
    )

    backend = create_web_app(
        get_asp_resource_name(shop_id),
        get_web_app_resource_name(shop_id),
    )

    rg = await db.resource_group.create(
        {
            "api_url": f"https://{backend.default_host_name}",
            "database_id": database.id,
            "azure_blob_storage_id": storage.container_name,
            "web_app_id": backend.id,
        }
    )

    updated_shop = await db.shop.update({"resource_group_id": rg.id}, {"id": shop_id})

    return updated_shop
