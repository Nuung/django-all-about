import logging
from django.apps import AppConfig

logger = logging.getLogger('django')

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis.user'

    def ready(self) -> None:
        logger.info(f"{self.name} app started well")
        return super().ready()