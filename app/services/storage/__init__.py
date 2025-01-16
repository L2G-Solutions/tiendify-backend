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
    blob_service_client = BlobServiceClient(
        account_url=azure_storage_url, credential=credential
    )
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name
    )
    blob_client.delete_blob()
