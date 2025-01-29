import unittest
import asyncio
from app.services.keycloak.realm import create_keycloak_realm
from app.config.config import Settings

settings = Settings(
    KEYCLOAK_URL="http://localhost:8080/auth",
    KEYCLOAK_ADMIN_USER="admin",
    KEYCLOAK_ADMIN_PASSWORD="admin",
    KEYCLOAK_REALM_PREFIX="shop-",
)

class TestCreateKeycloakRealm(unittest.TestCase):
    def setUp(self):
        # Datos de prueba
        self.shop_id = "test-shop-123"

    async def async_create_realm(self):
        # Llamar a la función bajo prueba
        return await create_keycloak_realm(self.shop_id)

    def test_create_realm_success(self):
        # Ejecutar la corrutina en un bucle de eventos
        realm_name = asyncio.run(self.async_create_realm())

        # Verificar el resultado
        expected_realm_name = f"{settings.KEYCLOAK_REALM_PREFIX}{self.shop_id}"
        self.assertEqual(realm_name, expected_realm_name)

    async def async_delete_realm(self, realm_name: str):
        # Función para eliminar el realm después de la prueba
        async with aiohttp.ClientSession() as session:
            # Obtener token de administrador
            token_url = (
                f"{settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
            )
            auth_data = {
                "client_id": "admin-cli",
                "username": settings.KEYCLOAK_ADMIN_USER,
                "password": settings.KEYCLOAK_ADMIN_PASSWORD,
                "grant_type": "password",
            }

            async with session.post(token_url, data=auth_data) as resp:
                token_data = await resp.json()
                access_token = token_data["access_token"]

            # Eliminar realm
            realm_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}"
            headers = {"Authorization": f"Bearer {access_token}"}

            async with session.delete(realm_url, headers=headers) as resp:
                if resp.status != 204:
                    error = await resp.text()
                    raise Exception(f"Error deleting realm: {error}")

    def tearDown(self):
        # Limpiar: Eliminar el realm después de la prueba
        realm_name = f"{settings.KEYCLOAK_REALM_PREFIX}{self.shop_id}"
        asyncio.run(self.async_delete_realm(realm_name))
        print(f"Realm eliminado: {realm_name}")
