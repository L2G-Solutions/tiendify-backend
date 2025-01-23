from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.web.models import AppServicePlan, Site, SiteConfig, SkuDescription

from app.config.config import settings
from app.services.azure.provisioning import credential


def create_web_app(
    app_service_plan_name: str,
    web_app_name: str,
    region: str = settings.AZURE_DEFAULT_REGION,
    sku_name: str = settings.AZURE_WEBAPP_DEFAULT_SKU,
    sku_tier: str = settings.AZURE_WEBAPP_DEFAULT_TIER,
    docker_image: str = settings.SHOPS_BACKEND_DOCKER_IMAGE,
) -> Site:
    web_client = WebSiteManagementClient(credential, settings.AZURE_SUBSCRIPTION_ID)

    app_service_plan = web_client.app_service_plans.begin_create_or_update(
        settings.AZURE_RESOURCE_GROUP,
        app_service_plan_name,
        AppServicePlan(
            location=region,
            sku=SkuDescription(name=sku_name, tier=sku_tier, capacity=1),
            reserved=True,
        ),
    ).result()

    web_app = web_client.web_apps.begin_create_or_update(
        settings.AZURE_RESOURCE_GROUP,
        web_app_name,
        Site(
            location=region,
            server_farm_id=app_service_plan.id,
            site_config=SiteConfig(
                linux_fx_version=f"DOCKER|{docker_image}",
            ),
        ),
    ).result()

    return web_app
