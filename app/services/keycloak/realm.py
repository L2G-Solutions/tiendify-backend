import aiohttp
from app.config.config import settings

async def create_keycloak_realm(shop_id: str) -> str:
    realm_name = f"{settings.KEYCLOAK_REALM_PREFIX}{shop_id}"
    
    async with aiohttp.ClientSession() as session:
        # Obtener token de administrador
        token_url = f"{settings.KEYCLOAK_URL}/realms/master/protocol/openid-connect/token"
        auth_data = {
            "client_id": "admin-cli",
            "username": settings.KEYCLOAK_ADMIN_USER,
            "password": settings.KEYCLOAK_ADMIN_PASSWORD,
            "grant_type": "password"
        }
        
        async with session.post(token_url, data=auth_data) as resp:
            token_data = await resp.json()
            access_token = token_data["access_token"]

        # Crear nuevo realm
        realm_url = f"{settings.KEYCLOAK_URL}/admin/realms"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        realm_config = {
            "realm": realm_name,
            "enabled": True,
            "registrationAllowed": True,
            "loginWithEmailAllowed": True
        }

        async with session.post(realm_url, json=realm_config, headers=headers) as resp:
            if resp.status not in [201, 409]:
                error = await resp.text()
                raise Exception(f"Error creating realm: {error}")
                
    return realm_name