from django.db import migrations


def backfill(apps, schema_editor):
    """Users created before StudentProfile/UserSettings existed (e.g. the first superuser)."""
    User = apps.get_model("accounts", "User")
    StudentProfile = apps.get_model("accounts", "StudentProfile")
    UserSettings = apps.get_model("accounts", "UserSettings")
    for user in User.objects.all():
        StudentProfile.objects.get_or_create(user=user)
        UserSettings.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_student_profile_and_settings"),
    ]

    operations = [
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
