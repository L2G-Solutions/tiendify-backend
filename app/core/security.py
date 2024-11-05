from keycloak import KeycloakOpenID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.config.config import settings
from jwt import PyJWKClient, decode
import jwt
from typing import Annotated

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
    authorizationUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
    refreshUrl=f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)

async def valid_access_token(access_token: str = Depends(oauth2_scheme)):
    jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(jwks_url)
    
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        print(f"Signing key: {signing_key.key}")
        
        decoded_token = decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=["account"],
            options={"verify_exp": True},
        )

        # if "realm_access" in decoded_token:
        #     if "access" not in decoded_token["realm_access"].get("roles", []):
        #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return decoded_token

    except jwt.exceptions.InvalidTokenError as e:
        print(f"Invalid token: {str(e)}")
        raise HTTPException(status_code=401, detail="Not authenticated")


def has_role(role_name: str):
    async def check_role(
        token_data: Annotated[dict, Depends(valid_access_token)]
    ):
        resource_access = token_data.get("resource_access")
        
        if not resource_access or "tiendify" not in resource_access or "roles" not in resource_access["tiendify"]:
            raise HTTPException(status_code=403, detail="No roles found in token")
        
        roles = resource_access["tiendify"]["roles"]
        
        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


