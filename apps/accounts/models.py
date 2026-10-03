from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^\+?[0-9][0-9 \-()]{6,19}$",
    message="Enter a valid phone number, for example +63 917 555 4821.",
)

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class User(AbstractUser):
    """Custom user. Identity and login only; clinic data lives on StudentProfile."""

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def first_display_name(self):
        return self.first_name or self.username


class StudentProfile(models.Model):
    """Medical and identification details (prototype: S.pro).

    Name and email stay on User so there is one source of truth for them.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    course = models.CharField(max_length=120, blank=True)
    year_level = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=25, blank=True, validators=[phone_validator])

    blood_type = models.CharField(max_length=3, blank=True)
    allergies = models.CharField(max_length=255, blank=True)
    notes = models.TextField("Conditions & notes", blank=True)

    emergency_name = models.CharField(max_length=120, blank=True)
    emergency_relationship = models.CharField(max_length=60, blank=True)
    emergency_phone = models.CharField(
        max_length=25, blank=True, validators=[phone_validator]
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.display_name} ({self.student_id or 'no ID'})"

    @property
    def has_allergy(self):
        return bool(self.allergies.strip())

    @property
    def has_emergency_contact(self):
        return bool(self.emergency_name.strip() and self.emergency_phone.strip())


class UserSettings(models.Model):
    """Per-student preferences (prototype: S.set). Defaults match the prototype."""

    TOGGLE_FIELDS = (
        "sms_alerts",
        "email_reminders",
        "queue_sound",
        "auto_triage",
        "share_anon_stats",
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings"
    )
    sms_alerts = models.BooleanField(default=True)
    email_reminders = models.BooleanField(default=True)
    queue_sound = models.BooleanField(default=False)
    auto_triage = models.BooleanField(default=True)
    share_anon_stats = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user settings"
        verbose_name_plural = "user settings"

    def __str__(self):
        return f"Settings for {self.user.display_name}"
