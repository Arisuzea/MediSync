from django.apps import AppConfig
from django.db.models.signals import post_migrate

ADMIN_PERMISSIONS = [
    "view_user", "add_user", "change_user",
    "view_activitylog",
    "view_volunteeragreement", "add_volunteeragreement", "change_volunteeragreement",
]


def grant_admin_group_permissions(sender, **kwargs):
    """System Administrator: accounts, roles, logs. No patient data (PLAN section 3.2)."""
    from django.contrib.auth.models import Group, Permission

    from .signals import ADMIN_GROUP

    group, _ = Group.objects.get_or_create(name=ADMIN_GROUP)
    group.permissions.set(
        Permission.objects.filter(content_type__app_label="accounts", codename__in=ADMIN_PERMISSIONS)
    )


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    def ready(self):
        from . import signals  # noqa: F401

        # sender=self runs after the auth app has created this app's permissions.
        post_migrate.connect(grant_admin_group_permissions, sender=self)
