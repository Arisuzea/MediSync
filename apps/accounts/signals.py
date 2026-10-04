from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import activity
from .models import PATIENT_ROLES, Patient, Role, UserSettings

ADMIN_GROUP = "System Administrator"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_related_rows(sender, instance, created, update_fields=None, **kwargs):
    """Every user gets a settings row; students and employees also get a Patient record,
    so views never hit DoesNotExist. Staff accounts are not patients."""
    if created:
        UserSettings.objects.get_or_create(user=instance)
    if created or update_fields is None or "role" in update_fields:
        if instance.role in PATIENT_ROLES:
            patient, made = Patient.objects.get_or_create(
                user=instance, defaults={"patient_type": instance.role}
            )
            if not made and patient.patient_type != instance.role:
                Patient.objects.filter(pk=patient.pk).update(patient_type=instance.role)
        if instance.role == Role.ADMIN:
            group, _ = Group.objects.get_or_create(name=ADMIN_GROUP)
            instance.groups.add(group)


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    activity.log_activity(user, activity.LOGIN, "accounts", user.pk)


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    activity.log_activity(user, activity.LOGOUT, "accounts", getattr(user, "pk", ""))


@receiver(user_login_failed)
def log_login_failed(sender, credentials, **kwargs):
    # Never store the password. The username helps spot guessing against one account.
    activity.log_activity(None, activity.LOGIN_FAILED, "accounts",
                          detail=f"username={credentials.get('username', '')}")
