import unittest
import uuid

import aiohttp

from app.config.config import Settings
from app.services.keycloak.realm import create_keycloak_realm


class TestCreateKeycloakRealm(unittest.IsolatedAsyncioTestCase):
    """Tests the creation of a Keycloak realm."""

    @classmethod
    def setUpClass(cls):
        cls.settings = Settings(
            KEYCLOAK_URL="http://localhost:8080",
            KEYCLOAK_ADMIN_USER="admin",
            KEYCLOAK_ADMIN_PASSWORD="admin",
            KEYCLOAK_REALM_PREFIX="shop-",
        )

    async def asyncSetUp(self):
        self.shop_id = f"test-shop-{uuid.uuid4()}"

    async def asyncTearDown(self):
        realm_name = f"{self.settings.KEYCLOAK_REALM_PREFIX}{self.shop_id}"
        try:
            await self.async_delete_realm(realm_name)
            print(f"Realm eliminado: {realm_name}")
        except Exception as e:
            print(f"Error en tearDown al eliminar realm: {e}")

    async def async_delete_realm(self, realm_name: str):
        async with aiohttp.ClientSession() as session:
            # Obtener token de administrador
            token_url = f"{self.settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
            auth_data = {
                "client_id": "admin-cli",
                "username": self.settings.KEYCLOAK_ADMIN_USER,
                "password": self.settings.KEYCLOAK_ADMIN_PASSWORD,
                "grant_type": "password",
            }

            async with session.post(token_url, data=auth_data) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    raise Exception(f"Error obteniendo token: {error}")
                token_data = await resp.json()
                access_token = token_data.get("access_token")
                if not access_token:
                    raise Exception("No se pudo obtener el token de administrador.")

            # Eliminar realm
            realm_url = f"{self.settings.KEYCLOAK_URL}/admin/realms/{realm_name}"
            headers = {"Authorization": f"Bearer {access_token}"}

            async with session.delete(realm_url, headers=headers) as resp:
                if resp.status != 204:
                    error = await resp.text()
                    raise Exception(f"Error eliminando realm: {error}")

    async def test_create_realm_success(self):
        """
        Prueba que verifica la creación exitosa de un realm en Keycloak.
        """
        keycloak_info = await create_keycloak_realm(self.shop_id)
        print(f"keycloak_info: {keycloak_info}")

        # Verificar que el realm_name es el esperado
        expected_realm_name = f"{self.settings.KEYCLOAK_REALM_PREFIX}{self.shop_id}"
        self.assertEqual(
            keycloak_info["realm_name"],
            expected_realm_name,
            f"El nombre del realm no coincide: {keycloak_info['realm_name']} != {expected_realm_name}",
        )

        # Verificar que client_id y client_secret no estén vacíos
        self.assertIsNotNone(
            keycloak_info.get("client_id"), "client_id no debe ser None."
        )
        self.assertIsNotNone(
            keycloak_info.get("client_secret"), "client_secret no debe ser None."
        )
        self.assertNotEqual(
            keycloak_info["client_id"], "", "client_id no debe estar vacío."
        )
        self.assertNotEqual(
            keycloak_info["client_secret"], "", "client_secret no debe estar vacío."
        )

        # Verificar que el realm realmente exista en Keycloak
        realm_exists = await self.check_realm_exists(expected_realm_name)
        self.assertTrue(
            realm_exists, f"El realm '{expected_realm_name}' no existe en Keycloak."
        )

    async def check_realm_exists(self, realm_name: str) -> bool:
        """
        Función para verificar si un realm existe en Keycloak.
        """
        async with aiohttp.ClientSession() as session:
            token_url = f"{self.settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
            auth_data = {
                "client_id": "admin-cli",
                "username": self.settings.KEYCLOAK_ADMIN_USER,
                "password": self.settings.KEYCLOAK_ADMIN_PASSWORD,
                "grant_type": "password",
            }

            async with session.post(token_url, data=auth_data) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    print(f"Error obteniendo token para verificar realm: {error}")
                    return False
                token_data = await resp.json()
                access_token = token_data.get("access_token")
                if not access_token:
                    print(
                        "No se pudo obtener el token de administrador para verificar realm."
                    )
                    return False

            realm_url = f"{self.settings.KEYCLOAK_URL}/admin/realms/{realm_name}"
            headers = {"Authorization": f"Bearer {access_token}"}

            async with session.get(realm_url, headers=headers) as resp:
                if resp.status == 200:
                    return True
                else:
                    error = await resp.text()
                    print(
                        f"Verificación de existencia del realm falló con status {resp.status}: {error}"
                    )
                    return False

    async def test_create_realm_already_exists(self):
        """
        Prueba que verifica el comportamiento cuando se intenta crear un realm que ya existe.
        """
        # Crear el realm por primera vez
        keycloak_info_1 = await create_keycloak_realm(self.shop_id)
        print(f"Primera creación: {keycloak_info_1}")

        # Intentar crear el realm nuevamente
        keycloak_info_2 = await create_keycloak_realm(self.shop_id)
        print(f"Segunda creación: {keycloak_info_2}")

        # Verificar que ambos resultados tengan el mismo realm_name
        expected_realm_name = f"{self.settings.KEYCLOAK_REALM_PREFIX}{self.shop_id}"
        self.assertEqual(
            keycloak_info_2["realm_name"],
            expected_realm_name,
            f"El nombre del realm no coincide en la segunda creación: {keycloak_info_2['realm_name']} != {expected_realm_name}",
        )

        # Verificar que client_id y client_secret sean los mismos si la función así lo maneja
        self.assertEqual(
            keycloak_info_2["client_id"],
            keycloak_info_1["client_id"],
            "client_id debería ser el mismo en re-creaciones.",
        )
        self.assertEqual(
            keycloak_info_2["client_secret"],
            keycloak_info_1["client_secret"],
            "client_secret debería ser el mismo en re-creaciones.",
        )


if __name__ == "__main__":
    unittest.main()
