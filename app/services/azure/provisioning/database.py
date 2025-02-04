from azure.mgmt.rdbms.postgresql_flexibleservers import PostgreSQLManagementClient
from azure.mgmt.rdbms.postgresql_flexibleservers.models import Server, Sku, Storage

from app.config.config import settings
from app.services.azure.provisioning import credential


def create_postgresql_database(
    server_name: str,
    admin_user: str,
    admin_password: str,
    region: str = settings.AZURE_DEFAULT_REGION,
    storage_size: int = 32,
    pg_version: str = "16",
) -> Server:
    """
    Creates a PostgreSQL database resource in Azure.

    Args:
        server_name (str): Name of the PostgreSQL server.
        admin_user (str): Administrator username for the PostgreSQL server.
        admin_password (str): Administrator password for the PostgreSQL server.
        region (str): Azure region (e.g., 'eastus'). Defaults to settings.AZURE_DEFAULT_REGION.

    Returns:
        Server: The created PostgreSQL server resource.
    """
    postgresql_client = PostgreSQLManagementClient(
        credential, settings.AZURE_SUBSCRIPTION_ID
    )
    server_parameters = Server(
        location=region,
        administrator_login=admin_user,
        administrator_login_password=admin_password,
        version=pg_version,
        storage=Storage(storage_size_gb=storage_size),
        sku=Sku(
            name=settings.AZURE_DB_DEFAULT_SKU,
            tier=settings.AZURE_DB_DEFAULT_TIER,
        ),
    )

    server = postgresql_client.servers.begin_create(
        resource_group_name=settings.AZURE_RESOURCE_GROUP,
        server_name=server_name,
        parameters=server_parameters,
    ).result()

    return server
