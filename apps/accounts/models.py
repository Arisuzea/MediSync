from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^\+?[0-9][0-9 \-()]{6,19}$",
    message="Enter a valid phone number, for example +63 917 555 4821.",
)

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class Role(models.TextChoices):
    STUDENT = "student", "Student"
    EMPLOYEE = "employee", "Employee"
    NURSE = "nurse", "Nurse"
    DOCTOR = "doctor", "Doctor"
    DENTIST = "dentist", "Dentist"
    VOLUNTEER = "volunteer", "Student volunteer"
    ADMIN = "admin", "System administrator"


PATIENT_ROLES = (Role.STUDENT, Role.EMPLOYEE)  # self-service users with a Patient record
STAFF_ROLES = (Role.NURSE, Role.DOCTOR, Role.DENTIST, Role.VOLUNTEER, Role.ADMIN)


class MediSyncUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra):
        extra.setdefault("role", Role.ADMIN)
        return super().create_superuser(username, email, password, **extra)


class User(AbstractUser):
    """Custom user. Identity, login and role; clinic data lives on Patient."""

    role = models.CharField(max_length=12, choices=Role.choices, default=Role.STUDENT)

    objects = MediSyncUserManager()

    @property
    def is_patient_role(self):
        return self.role in PATIENT_ROLES

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def first_display_name(self):
        return self.first_name or self.username

    def save(self, *args, **kwargs):
        # The admin site requires is_staff; the role decides who actually gets in.
        if self.role == Role.ADMIN and not self.is_staff:
            self.is_staff = True
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = {*kwargs["update_fields"], "is_staff"}
        super().save(*args, **kwargs)


class Patient(models.Model):
    """One clinic identity per person (prototype: S.pro).

    Account holders (students, employees) link to a User, which owns their name and
    email. Outside visitors have no User; staff register them and `full_name` holds
    their name.
    """

    class PatientType(models.TextChoices):
        STUDENT = "student", "Student"
        EMPLOYEE = "employee", "Employee"
        VISITOR = "visitor", "Outside visitor"

    class Sex(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile",
        null=True, blank=True,
    )
    patient_type = models.CharField(
        max_length=10, choices=PatientType.choices, default=PatientType.STUDENT
    )
    full_name = models.CharField(
        max_length=300, blank=True, help_text="Only for visitors. Account holders use their User name."
    )
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, blank=True)
    address = models.CharField(max_length=255, blank=True)
    guardian_name = models.CharField(max_length=120, blank=True)
    guardian_phone = models.CharField(max_length=25, blank=True, validators=[phone_validator])

    consent_agreed = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)

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

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(user__isnull=False) | ~models.Q(full_name=""),
                name="patient_has_user_or_name",
            ),
        ]

    @property
    def display_name(self):
        return self.user.display_name if self.user_id else self.full_name

    def __str__(self):
        return f"{self.display_name} ({self.student_id or 'no ID'})"

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


class ActivityLog(models.Model):
    """Append-only audit trail. Write through apps.accounts.activity.log_activity."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="activity",
    )
    action = models.CharField(max_length=40)
    module = models.CharField(max_length=40, blank=True)
    object_id = models.CharField(max_length=40, blank=True)
    detail = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.user_id or '-'} {self.action}"


class VolunteerAgreement(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SIGNED = "signed", "Signed"
        REVOKED = "revoked", "Revoked"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="volunteer_agreements"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    signed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.display_name}: {self.status}"
