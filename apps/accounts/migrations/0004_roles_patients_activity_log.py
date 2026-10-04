"""Stage 3: user roles, StudentProfile -> Patient (data kept), ActivityLog, VolunteerAgreement."""

import apps.accounts.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

PHONE = django.core.validators.RegexValidator(
    message="Enter a valid phone number, for example +63 917 555 4821.",
    regex="^\\+?[0-9][0-9 \\-()]{6,19}$",
)


def set_roles(apps, schema_editor):
    """Existing superusers become System Administrators; everyone else stays a student."""
    User = apps.get_model("accounts", "User")
    User.objects.filter(is_superuser=True).update(role="admin")
    # Staff are not patients: drop the blank profile the old signal gave them.
    Profile = apps.get_model("accounts", "StudentProfile")
    Profile.objects.filter(
        user__role="admin", student_id__isnull=True, course="", phone="", allergies="", notes=""
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_backfill_profiles"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[("objects", apps.accounts.models.MediSyncUserManager())],
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("student", "Student"),
                    ("employee", "Employee"),
                    ("nurse", "Nurse"),
                    ("doctor", "Doctor"),
                    ("dentist", "Dentist"),
                    ("volunteer", "Student volunteer"),
                    ("admin", "System administrator"),
                ],
                default="student",
                max_length=12,
            ),
        ),
        migrations.RunPython(set_roles, migrations.RunPython.noop),
        # A rename keeps every existing row.
        migrations.RenameModel(old_name="StudentProfile", new_name="Patient"),
        migrations.AlterField(
            model_name="patient",
            name="user",
            field=models.OneToOneField(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name="profile", to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="patient_type",
            field=models.CharField(
                choices=[("student", "Student"), ("employee", "Employee"), ("visitor", "Outside visitor")],
                default="student", max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="full_name",
            field=models.CharField(
                blank=True, max_length=300,
                help_text="Only for visitors. Account holders use their User name.",
            ),
        ),
        migrations.AddField(model_name="patient", name="birth_date", field=models.DateField(blank=True, null=True)),
        migrations.AddField(
            model_name="patient",
            name="sex",
            field=models.CharField(blank=True, choices=[("F", "Female"), ("M", "Male")], max_length=1),
        ),
        migrations.AddField(model_name="patient", name="address", field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name="patient", name="guardian_name", field=models.CharField(blank=True, max_length=120)),
        migrations.AddField(
            model_name="patient",
            name="guardian_phone",
            field=models.CharField(blank=True, max_length=25, validators=[PHONE]),
        ),
        migrations.AddField(model_name="patient", name="consent_agreed", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="patient", name="consent_date", field=models.DateTimeField(blank=True, null=True)),
        migrations.AddConstraint(
            model_name="patient",
            constraint=models.CheckConstraint(
                condition=models.Q(("user__isnull", False), models.Q(("full_name", ""), _negated=True), _connector="OR"),
                name="patient_has_user_or_name",
            ),
        ),
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=40)),
                ("module", models.CharField(blank=True, max_length=40)),
                ("object_id", models.CharField(blank=True, max_length=40)),
                ("detail", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                        related_name="activity", to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="VolunteerAgreement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("signed", "Signed"), ("revoked", "Revoked")],
                        default="pending", max_length=10,
                    ),
                ),
                ("signed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="volunteer_agreements", to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
