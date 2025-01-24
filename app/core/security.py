from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jwt import PyJWKClient, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from keycloak import KeycloakOpenID

from app.config.config import settings
from app.models.auth import UserTokenInfo

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)


cookie_scheme = APIKeyCookie(name="access_token")


async def valid_access_token(access_token: str = Depends(cookie_scheme)):
    jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    jwks_client = PyJWKClient(jwks_url, timeout=10)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)

        decoded_token = decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=["account"],
            options={"verify_exp": True},
        )

        return decoded_token
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")


def has_role(role_name: str):
    async def check_role(token_data: Annotated[dict, Depends(valid_access_token)]):
        resource_access = token_data.get("resource_access")

        if (
            not resource_access
            or "tiendify" not in resource_access
            or "roles" not in resource_access["tiendify"]
        ):
            raise HTTPException(status_code=403, detail="No roles found in token")

        roles = resource_access["tiendify"]["roles"]

        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


async def get_current_user(
    token_data: Annotated[dict, Depends(valid_access_token)]
) -> UserTokenInfo:
    try:
        user_info = {
            "username": token_data.get("preferred_username"),
            "email": token_data.get("email"),
            "firstName": token_data.get("given_name"),
            "lastName": token_data.get("family_name"),
        }
        return UserTokenInfo(**user_info)
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid token structure")
