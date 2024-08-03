from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db import transaction, DEFAULT_DB_ALIAS, connections


class ExplorerAppConfig(AppConfig):

    name = "explorer"
    verbose_name = _("SQL Explorer")
    default_auto_field = "django.db.models.AutoField"


def new_get_connection(using=None):
    from explorer.ee.db_connections.models import DatabaseConnection
    if using is None:
        using = DEFAULT_DB_ALIAS
    if using in connections:
        return connections[using]
    return DatabaseConnection.objects.get(alias=using).as_django_connection()


# Monkey patch
transaction.get_connection = new_get_connection
