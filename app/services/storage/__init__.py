from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from app.config.config import settings

credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
    account_url=settings.AZURE_STORAGE, credential=credential
)


def upload_file(file: bytes, file_name: str, overwrite=True) -> dict:
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_PUBLIC_CONTAINER, blob=file_name
    )
    return blob_client.upload_blob(file, overwrite=overwrite)


def delete_file(file_name: str) -> None:
    blob_client = blob_service_client.get_blob_client(
        container=settings.AZURE_PUBLIC_CONTAINER, blob=file_name
    )
    blob_client.delete_blob()
