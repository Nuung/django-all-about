import logging
from django.apps import AppConfig

logger = logging.getLogger("django")


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apis.products"

    def ready(self) -> None:
        logger.info(f"{self.name} app started well")
        return super().ready()
