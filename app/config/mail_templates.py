from fastapi import Request
from fastapi.templating import Jinja2Templates


class MailTemplates:
    """Class for rendering email HTML templates using Jinja2Templates."""

    def __init__(self):
        self.templates = Jinja2Templates(directory="app/templates/emails")

    def _render(self, template: str, **kwargs):
        request = Request(scope={"type": "http", "path": "/"}, receive=None)
        return self.templates.TemplateResponse(
            template,
            {"request": request, **kwargs},
        ).body.decode()

    def render_store_created_template(self, user_name: str, store_name: str):
        return self._render(
            "store_created.html", user_name=user_name, store_name=store_name
        )
