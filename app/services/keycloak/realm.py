import aiohttp

from app.config.config import settings


async def create_keycloak_realm(shop_id: str) -> dict:
    realm_name = f"{settings.KEYCLOAK_REALM_PREFIX}{shop_id}"

    async with aiohttp.ClientSession() as session:
        # 1. Obtener token de administrador
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

        # 2. Crear nuevo realm
        realm_url = f"{settings.KEYCLOAK_URL}/admin/realms"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        realm_config = {
            "realm": realm_name,
            "enabled": True,
            "registrationAllowed": True,
            "loginWithEmailAllowed": True,
        }

        async with session.post(realm_url, json=realm_config, headers=headers) as resp:
            print(f"Crear realm response status: {resp.status}")
            if resp.status not in [201, 409]:
                error = await resp.text()
                print(f"Error creando realm: {error}")
                raise Exception(f"Error creando realm: {error}")
            else:
                print(f"Realm creado o ya existente con status: {resp.status}")

        # 3. Crear cliente administrador con cuentas de servicio habilitadas
        client_config = {
            "clientId": "admin-client",
            "enabled": True,
            "protocol": "openid-connect",
            "redirectUris": [],
            "directAccessGrantsEnabled": False,
            "serviceAccountsEnabled": True,
            "publicClient": False,
            "protocolMappers": [],
            "attributes": {},
        }

        client_creation_url = (
            f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients"
        )
        async with session.post(
            client_creation_url, json=client_config, headers=headers
        ) as resp:
            print(f"Crear cliente response status: {resp.status}")
            if resp.status == 201:
                client_location = resp.headers.get("Location")
                if not client_location:
                    raise Exception(
                        "Respuesta de creación de cliente sin encabezado Location"
                    )
                client_id = client_location.split("/")[-1]
                print(f"Cliente creado con ID: {client_id}")
            elif resp.status == 409:
                # Cliente ya existe, buscar su ID
                print("Cliente ya existe, buscando su ID")
                clients_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients?clientId=admin-client"
                async with session.get(clients_url, headers=headers) as list_resp:
                    if list_resp.status != 200:
                        error = await list_resp.text()
                        raise Exception(f"Error listando clientes: {error}")
                    clients = await list_resp.json()
                    if not clients:
                        raise Exception(
                            "Cliente 'admin-client' no encontrado después de conflicto."
                        )
                    client_id = clients[0]["id"]
                    print(f"Cliente existente encontrado con ID: {client_id}")
            else:
                error = await resp.text()
                raise Exception(f"Error creando cliente: {error}")

        # 4. Obtener el usuario de cuenta de servicio del cliente
        service_account_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients/{client_id}/service-account-user"
        async with session.get(service_account_url, headers=headers) as resp:
            print(f"Obtener service account response status: {resp.status}")
            if resp.status != 200:
                error = await resp.text()
                raise Exception(f"Error obteniendo service account user: {error}")
            service_account = await resp.json()
            service_account_id = service_account["id"]
            print(f"Service account user ID: {service_account_id}")

        # 5. Obtener cliente 'realm-management'
        realm_management_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients?clientId=realm-management"
        async with session.get(realm_management_url, headers=headers) as resp:
            print(f"Obtener cliente 'realm-management' response status: {resp.status}")
            if resp.status != 200:
                error = await resp.text()
                raise Exception(f"Error obteniendo cliente 'realm-management': {error}")
            clients = await resp.json()
            if not clients:
                raise Exception("Cliente 'realm-management' no encontrado.")
            realm_management_id = clients[0]["id"]
            print(f"Cliente 'realm-management' ID: {realm_management_id}")

        # 6. Obtener roles disponibles en 'realm-management'
        roles_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients/{realm_management_id}/roles"
        async with session.get(roles_url, headers=headers) as resp:
            print(f"Obtener roles de 'realm-management' response status: {resp.status}")
            if resp.status != 200:
                error = await resp.text()
                raise Exception(
                    f"Error obteniendo roles de 'realm-management': {error}"
                )
            roles = await resp.json()
            role_names = [role["name"] for role in roles]

        # 7. Definir roles requeridos y filtrar
        required_roles = ["manage-users", "view-realm", "manage-realm"]
        roles_to_assign = [role for role in roles if role["name"] in required_roles]

        if not roles_to_assign:
            raise Exception(
                "No se encontraron los roles requeridos para asignar al cliente."
            )

        # 8. Asignar roles al usuario de cuenta de servicio (usando la ruta de client roles)
        assign_roles_url = (
            f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/users/"
            f"{service_account_id}/role-mappings/clients/{realm_management_id}"
        )
        async with session.post(
            assign_roles_url, json=roles_to_assign, headers=headers
        ) as resp:
            print(f"Asignar roles response status: {resp.status}")
            if resp.status != 204:
                error = await resp.text()
                raise Exception(
                    f"Error asignando roles al service account user: {error}"
                )
            print("Roles asignados al service account user.")

        # 9. Obtener secreto del cliente
        client_secret_url = f"{settings.KEYCLOAK_URL}/admin/realms/{realm_name}/clients/{client_id}/client-secret"
        async with session.get(client_secret_url, headers=headers) as resp:
            print(f"Obtener secreto cliente response status: {resp.status}")
            if resp.status != 200:
                error = await resp.text()
                print(f"Error obteniendo secreto del cliente: {error}")
                raise Exception(f"Error obteniendo secreto del cliente: {error}")
            secret_data = await resp.json()
            client_secret = secret_data.get("value")
            if not client_secret:
                raise Exception("Secreto del cliente no encontrado en la respuesta")

    # Retornar el nombre del realm y las credenciales del cliente
    return {
        "realm_name": realm_name,
        "client_id": client_id,
        "client_secret": client_secret,
    }
