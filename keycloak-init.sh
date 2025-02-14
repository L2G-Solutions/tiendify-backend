#!/bin/bash
set -e

KEYCLOAK_URL="http://identity:7080"
REALM="master"
CLIENT_ID="tiendify"
ADMIN_USER="admin"
ADMIN_PASS="admin"

echo "Waiting for Keycloak to be ready..."
until curl -s $KEYCLOAK_URL/realms/master | grep '"realm"'; do
  sleep 5
done

echo "Logging into Keycloak..."
TOKEN=$(curl -s -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$ADMIN_USER" \
  -d "password=$ADMIN_PASS" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r .access_token)

echo "Retrieving client UUID..."
CLIENT_UUID=$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM/clients?clientId=$CLIENT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq -r '.[0].id')

echo "Retrieving client secret..."
CLIENT_SECRET=$(curl -s -X GET "$KEYCLOAK_URL/admin/realms/$REALM/clients/$CLIENT_UUID/client-secret" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq -r .value)

echo "Client Secret: $CLIENT_SECRET"

echo "Starting API with retrieved secret..."
export KEYCLOAK_CLIENT_SECRET=$CLIENT_SECRET
exec "$@"
