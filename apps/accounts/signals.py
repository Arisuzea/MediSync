from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentProfile, UserSettings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_related_rows(sender, instance, created, **kwargs):
    """Every user gets a profile and a settings row, so views never hit DoesNotExist."""
    if created:
        StudentProfile.objects.get_or_create(user=instance)
        UserSettings.objects.get_or_create(user=instance)
