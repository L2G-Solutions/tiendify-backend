import unittest

from app.services.azure.provisioning.database import create_postgresql_database


class TestCreatePostgresqlDatabase(unittest.TestCase):
    """Test the creation of a PostgreSQL database in Azure."""

    def test_create_postgresql_database(self):
        server_name = "tiendify-postgresql-test"
        region = "westus"
        admin_user = "usertesting123"
        admin_password = "userpassword123"

        server_details = create_postgresql_database(
            server_name,
            admin_user,
            admin_password,
            region,
        )

        self.assertEqual(server_details.name, server_name)
