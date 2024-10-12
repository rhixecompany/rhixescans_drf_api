import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.apps"
    verbose_name = _("Apps")

    def ready(self):
        with contextlib.suppress(ImportError):
            import api.apps.signals  # noqa: F401
