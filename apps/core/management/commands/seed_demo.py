"""Recreate the prototype's demo data.  Safe to run repeatedly.

    python manage.py seed_demo

Stage 2 seeds the demo student only. Later stages add practitioners,
visit reasons, symptoms, FAQs and sample appointments here.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

DEMO_USERNAME = "alex.mendoza"
DEMO_PASSWORD = "medisync-demo"  # development only, printed below


class Command(BaseCommand):
    help = "Create or refresh the demo student from the prototype."

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=DEMO_USERNAME,
            defaults={
                "first_name": "Alex",
                "last_name": "Mendoza",
                "email": "alex.mendoza@university.edu",
            },
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()

        p = user.profile
        p.student_id = "2023-11482"
        p.course = "BS Computer Science"
        p.year_level = "3rd Year"
        p.phone = "+63 917 555 4821"
        p.blood_type = "O+"
        p.allergies = "Penicillin"
        p.notes = "Mild asthma — carries inhaler."
        p.emergency_name = "Maria Reyes"
        p.emergency_relationship = "Mother"
        p.emergency_phone = "+63 917 555 1180"
        p.save()

        self.stdout.write(self.style.SUCCESS(
            f"Demo student ready. Username: {DEMO_USERNAME}"
            + (f"  Password: {DEMO_PASSWORD}" if created else "  (existing password unchanged)")
        ))
