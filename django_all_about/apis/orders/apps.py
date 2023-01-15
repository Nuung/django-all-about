from django.apps import AppConfig
import logging

logger = logging.getLogger("django")


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apis.orders"

    def ready(self) -> None:
        logger.info(f"{self.name} app started well")
        return super().ready()
