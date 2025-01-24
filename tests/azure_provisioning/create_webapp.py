import unittest

from app.services.azure.provisioning.webapp import create_web_app


class TestCreateWebApp(unittest.TestCase):
    def test_create_web_app(self):
        app_service_plan_name = "test-asp"
        web_app_name = "test-was"
        region = "westus"
        sku_name = "B1"
        sku_tier = "Basic"
        docker_image = "nginx:latest"
        web_app = create_web_app(
            app_service_plan_name=app_service_plan_name,
            web_app_name=web_app_name,
            region=region,
            sku_name=sku_name,
            sku_tier=sku_tier,
            docker_image=docker_image,
        )
        self.assertEqual(web_app.name, web_app_name)
        self.assertEqual(web_app.location, region)
