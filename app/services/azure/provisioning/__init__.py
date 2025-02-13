from azure.identity import DefaultAzureCredential

# Azure authentication is managed by the DefaultAzureCredential class.
# This looks for environment variables, managed identity, or interactive login.
credential = DefaultAzureCredential()
