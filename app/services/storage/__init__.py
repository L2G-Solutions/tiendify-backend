from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()


def upload_file(
    file: bytes,
    file_name: str,
    azure_storage_url: str,
    container_name: str = "public",
    overwrite: bool = True,
) -> dict:
    """Upload a file to Azure Blob Storage.

    Args:
        file (bytes): File to upload.
        file_name (str): Name of the file.
        azure_storage_url (str): URL of the Azure Storage Account.
        container_name (str, optional): Blob container name. Defaults to "public".
        overwrite (bool, optional): Overwrite if file already exists. Defaults to True.

    Returns:
        dict: Upload response from Azure.
    """
    blob_service_client = BlobServiceClient(
        account_url=azure_storage_url, credential=credential
    )

    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )
    return blob_client.upload_blob(file, overwrite=overwrite)


def delete_file(
    file_name: str, azure_storage_url: str, container_name: str = "public"
) -> None:
    """Delete a file from Azure Blob Storage.

    Args:
        file_name (str): Name of the file.
        azure_storage_url (str): URL of the Azure Storage Account.
        container_name (str, optional): Blob container name. Defaults to "public".
    """
    blob_service_client = BlobServiceClient(
        account_url=azure_storage_url, credential=credential
    )
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )
    blob_client.delete_blob()
