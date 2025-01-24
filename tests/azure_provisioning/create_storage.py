import unittest

from app.services.azure.provisioning.storage import create_public_container


class TestCreateBlobStorageContainer(unittest.TestCase):
    def test_create_blob_storage_container(self):
        account_name = "tiendifyblobstoragetest"
        container_name = "test"
        container = create_public_container(account_name, container_name=container_name)
        self.assertEqual(container.container_name, container_name)
