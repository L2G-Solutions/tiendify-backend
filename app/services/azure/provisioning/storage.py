from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    AccessTier,
    Kind,
    Sku,
    StorageAccount,
    StorageAccountCreateParameters,
    StorageAccountUpdateParameters,
)
from azure.storage.blob import BlobServiceClient, ContainerClient, PublicAccess

from app.config.config import settings
from app.services.azure.provisioning import credential


def create_blob_storage_account(
    account_name: str,
    region: str = settings.AZURE_DEFAULT_REGION,
    allow_public_access: bool = True,
) -> StorageAccount:
    """
    Creates a Blob Storage Account in Azure.

    Args:
        account_name (str): Name of the storage account (must be globally unique).
        region (str): Azure region (e.g., 'eastus'). Defaults to `settings.AZURE_DEFAULT_REGION`.
        allow_public_access (bool): Whether to allow public access to blobs. Defaults to `True`.

    Returns:
        StorageAccount: The created storage account.
    """
    storage_client = StorageManagementClient(credential, settings.AZURE_SUBSCRIPTION_ID)

    storage_parameters = StorageAccountCreateParameters(
        sku=Sku(name=settings.AZURE_STORAGE_DEFAULT_SKU),
        kind=Kind.BLOB_STORAGE,
        location=region,
        access_tier=AccessTier.HOT,
    )

    storage_account = storage_client.storage_accounts.begin_create(
        resource_group_name=settings.AZURE_RESOURCE_GROUP,
        account_name=account_name,
        parameters=storage_parameters,
    ).result()

    if allow_public_access:
        storage_client.storage_accounts.update(
            resource_group_name=settings.AZURE_RESOURCE_GROUP,
            account_name=account_name,
            parameters=StorageAccountUpdateParameters(allow_blob_public_access=True),
        )

    return None


def create_public_container(
    account_name: str, container_name: str = "public"
) -> ContainerClient:
    storage_client = StorageManagementClient(credential, settings.AZURE_SUBSCRIPTION_ID)

    keys = storage_client.storage_accounts.list_keys(
        settings.AZURE_RESOURCE_GROUP, account_name
    )
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={keys.keys[0].value};EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.create_container(
        container_name, public_access=PublicAccess.BLOB
    )

    return container_client
