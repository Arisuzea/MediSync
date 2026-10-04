"""Recreate the prototype's demo data.  Safe to run repeatedly.

    python manage.py seed_demo

Seeds the demo student, one sample account per staff role and one visitor patient.
Later stages add practitioners, visit reasons, symptoms, FAQs and sample appointments.
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Patient, Role, VolunteerAgreement

DEMO_USERNAME = "alex.mendoza"
DEMO_PASSWORD = "medisync-demo"  # development only, printed below

# username, first name, last name, role
STAFF = [
    ("nurse.demo", "Joy", "Villanueva", Role.NURSE),
    ("doctor.demo", "Elena", "Reyes", Role.DOCTOR),
    ("dentist.demo", "Marco", "Tan", Role.DENTIST),
    ("volunteer.demo", "Pia", "Lim", Role.VOLUNTEER),
    ("admin.demo", "Sam", "Rivera", Role.ADMIN),
]


class Command(BaseCommand):
    help = "Create or refresh the demo student, sample staff accounts and a sample visitor."

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

        for username, first, last, role in STAFF:
            staff, made = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first, "last_name": last, "role": role,
                          "email": f"{username}@university.edu"},
            )
            if made:
                staff.set_password(DEMO_PASSWORD)
                staff.save()
            if role == Role.VOLUNTEER:
                VolunteerAgreement.objects.get_or_create(
                    user=staff, defaults={"status": "signed", "signed_at": timezone.now()}
                )

        # An outside visitor: no account, consent recorded by staff at the desk.
        Patient.objects.get_or_create(
            patient_type=Patient.PatientType.VISITOR, full_name="Jordan Visitor",
            defaults={"phone": "+63 917 555 0100", "consent_agreed": True,
                      "consent_date": timezone.now()},
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo accounts ready: " + ", ".join([DEMO_USERNAME] + [u for u, *_ in STAFF])
            + ". Sample visitor patient: Jordan Visitor."
        ))
        self.stdout.write(
            f"New accounts use the password {DEMO_PASSWORD}. Existing passwords are unchanged."
        )
