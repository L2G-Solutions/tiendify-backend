import aiohttp
import requests

from app.config.config import settings


async def get_keycloak_token():
    """Authenticates with Keycloak using the admin credentials and returns the access token.

    Raises:
        Exception: Could not get token.
        Exception: No access token.

    Returns:
        str: Access token.
    """
    async with aiohttp.ClientSession() as session:
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
            print(f"Obteniendo token response status: {resp.status}")
            if resp.status != 200:
                error = await resp.text()
                print(f"Error obteniendo token: {error}")
                raise Exception(f"Error obteniendo token: {error}")
            token_data = await resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                raise Exception("No se pudo obtener el token de administrador.")

        return access_token


async def create_keycloak_user(
    username: str, email: str, password: str, first_name: str, last_name: str
) -> bool:
    """Creates a new user in Keycloak.

    Args:
        username (str): Username, must be unique.
        email (str): Email.
        password (str): Password.
        first_name (str): First name.
        last_name (str): Last name.

    Returns:
        bool: True if user was created successfully, False otherwise.
    """
    access_token = await get_keycloak_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    user_data = {
        "username": username,
        "email": email,
        "enabled": True,
        "firstName": first_name,
        "lastName": last_name,
        "credentials": [
            {
                "type": "password",
                "value": password,
            }
        ],
    }

    res = requests.post(
        f"{settings.KEYCLOAK_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users",
        json=user_data,
        headers=headers,
    )

    return res.ok
