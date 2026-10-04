from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import IntegrityError, connection, transaction
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from . import activity
from .models import ActivityLog, Patient, Role, UserSettings, VolunteerAgreement

User = get_user_model()


def make_student(username="sam", student_id="2024-00001", password="pw-12345-xyz"):
    user = User.objects.create_user(username, password=password, first_name="Sam", last_name="Cruz")
    user.profile.student_id = student_id
    user.profile.consent_agreed = True  # most tests are not about the consent gate
    user.profile.save()
    return user


def make_user(role, username=None):
    return User.objects.create_user(username or role, password="pw-12345-xyz", role=role)


class SignalTests(TestCase):
    def test_new_user_gets_profile_and_settings(self):
        u = User.objects.create_user("new", password="x")
        self.assertTrue(Patient.objects.filter(user=u).exists())
        self.assertTrue(UserSettings.objects.filter(user=u).exists())

    def test_settings_defaults_match_prototype(self):
        s = User.objects.create_user("d", password="x").settings
        self.assertEqual(
            (s.sms_alerts, s.email_reminders, s.queue_sound, s.auto_triage, s.share_anon_stats),
            (True, True, False, True, False),
        )


class AuthTests(TestCase):
    def setUp(self):
        self.user = make_student()

    def test_pages_require_login(self):
        for name in ("core:dashboard", "accounts:profile", "accounts:settings",
                     "accounts:export", "accounts:password_change"):
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 302, name)
            self.assertIn(reverse("accounts:login"), resp["Location"], name)

    def test_toggle_requires_login_and_post(self):
        resp = self.client.post(reverse("accounts:toggle_setting"), {"setting": "sms_alerts"})
        self.assertEqual(resp.status_code, 302)
        self.assertIn("login", resp["Location"])
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:toggle_setting")).status_code, 405)

    def test_login_and_logout(self):
        resp = self.client.post(reverse("accounts:login"), {"username": "sam", "password": "pw-12345-xyz"})
        self.assertRedirects(resp, reverse("core:dashboard"), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("core:dashboard")).status_code, 200)
        resp = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(resp, reverse("accounts:login"), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("core:dashboard")).status_code, 302)

    def test_logout_needs_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)

    def test_bad_login_shows_error(self):
        resp = self.client.post(reverse("accounts:login"), {"username": "sam", "password": "wrong"})
        self.assertContains(resp, "Incorrect username or password")


class ProfileTests(TestCase):
    def setUp(self):
        self.user = make_student()
        self.client.force_login(self.user)
        self.url = reverse("accounts:profile")

    def payload(self, **over):
        data = {
            "full_name": "Sam Q. Cruz", "student_id": "2024-00001", "course": "BS IT",
            "year_level": "2nd Year", "email": "sam@example.com", "phone": "+63 917 555 0000",
            "blood_type": "o+", "allergies": "Peanuts", "notes": "",
        }
        data.update(over)
        return data

    def test_get_renders_with_values(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, "Medical profile")
        self.assertContains(resp, "2024-00001")

    def test_save_updates_user_and_profile(self):
        resp = self.client.post(self.url, self.payload())
        self.assertRedirects(resp, self.url, fetch_redirect_response=False)
        self.user.refresh_from_db()
        self.assertEqual((self.user.first_name, self.user.last_name), ("Sam Q.", "Cruz"))
        self.assertEqual(self.user.email, "sam@example.com")
        self.assertEqual(self.user.profile.blood_type, "O+")  # normalised
        self.assertEqual(self.user.profile.allergies, "Peanuts")

    def test_invalid_blood_type_rejected(self):
        resp = self.client.post(self.url, self.payload(blood_type="Z+"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Use one of")
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.blood_type, "")

    def test_student_id_must_be_unique(self):
        make_student("other", "2024-00002")
        resp = self.client.post(self.url, self.payload(student_id="2024-00002"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "already exists")

    def test_blank_student_ids_do_not_collide(self):
        a = User.objects.create_user("a", password="x")
        b = User.objects.create_user("b", password="x")
        self.assertIsNone(a.profile.student_id)
        self.assertIsNone(b.profile.student_id)

    def test_cannot_edit_someone_elses_profile(self):
        other = make_student("victim", "2024-00009")
        self.client.post(self.url, self.payload(student_id="2024-00001", course="Hacked"))
        other.refresh_from_db()
        self.assertNotEqual(other.profile.course, "Hacked")

    def test_emergency_contact(self):
        resp = self.client.post(reverse("accounts:emergency_contact"), {
            "emergency_name": "Maria Reyes", "emergency_relationship": "Mother",
            "emergency_phone": "+63 917 555 1180",
        })
        self.assertRedirects(resp, self.url, fetch_redirect_response=False)
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.has_emergency_contact)

    def test_emergency_contact_bad_phone(self):
        resp = self.client.post(reverse("accounts:emergency_contact"), {
            "emergency_name": "X", "emergency_relationship": "", "emergency_phone": "abc",
        })
        self.assertEqual(resp.status_code, 400)


class SettingsTests(TestCase):
    def setUp(self):
        self.user = make_student()
        self.client.force_login(self.user)

    def test_toggle_flips_value(self):
        self.assertFalse(self.user.settings.queue_sound)
        self.client.post(reverse("accounts:toggle_setting"), {"setting": "queue_sound"})
        self.user.settings.refresh_from_db()
        self.assertTrue(self.user.settings.queue_sound)
        self.client.post(reverse("accounts:toggle_setting"), {"setting": "queue_sound"})
        self.user.settings.refresh_from_db()
        self.assertFalse(self.user.settings.queue_sound)

    def test_unknown_key_rejected(self):
        self.client.post(reverse("accounts:toggle_setting"), {"setting": "user_id"})
        self.user.refresh_from_db()  # nothing blew up, nothing changed
        self.assertTrue(self.user.settings.sms_alerts)

    def test_toggle_only_affects_own_settings(self):
        other = make_student("o2", "2024-00003")
        self.client.post(reverse("accounts:toggle_setting"), {"setting": "sms_alerts"})
        other.settings.refresh_from_db()
        self.assertTrue(other.settings.sms_alerts)

    def test_settings_page_renders(self):
        self.assertContains(self.client.get(reverse("accounts:settings")), "SMS alerts")

    def test_export_is_own_data_json(self):
        resp = self.client.get(reverse("accounts:export"))
        self.assertEqual(resp["Content-Type"], "application/json")
        data = resp.json()
        self.assertEqual(data["account"]["username"], "sam")
        self.assertEqual(data["profile"]["student_id"], "2024-00001")


class ShellTests(TestCase):
    """The layout context processor must feed the sidebar, topbar and welcome banner."""

    def test_shell_shows_real_student_and_nav(self):
        user = make_student()
        user.profile.course = "BS Nursing"
        user.profile.save()
        self.client.force_login(user)
        html = self.client.get(reverse("core:dashboard")).content.decode()
        self.assertIn("Welcome back, Sam", html)
        self.assertIn("2024-00001 · BS Nursing", html)
        self.assertIn(reverse("accounts:profile"), html)
        self.assertIn("modal-signout", html)


PATIENT_URLS = ["core:dashboard", "core:help", "appointments:book", "appointments:practitioner",
                "appointments:schedule", "appointments:symptoms", "appointments:result",
                "appointments:confirmation", "appointments:queue", "appointments:history",
                "accounts:profile", "accounts:settings", "accounts:export", "accounts:password_change"]


class RoleTests(TestCase):
    def test_new_users_default_to_student(self):
        self.assertEqual(User.objects.create_user("x").role, Role.STUDENT)

    def test_create_superuser_is_admin_role(self):
        su = User.objects.create_superuser("root", password="x")
        self.assertEqual(su.role, Role.ADMIN)

    def test_admin_role_is_staff(self):
        self.assertTrue(make_user(Role.ADMIN).is_staff)

    def test_staff_get_no_patient_record_but_patients_do(self):
        self.assertFalse(Patient.objects.filter(user=make_user(Role.NURSE)).exists())
        emp = make_user(Role.EMPLOYEE)
        self.assertEqual(emp.profile.patient_type, "employee")

    def test_changing_role_updates_patient_type(self):
        u = make_student()
        u.role = Role.EMPLOYEE
        u.save()
        u.profile.refresh_from_db()
        self.assertEqual(u.profile.patient_type, "employee")

    def test_patient_roles_open_every_patient_page(self):
        for role in (Role.STUDENT, Role.EMPLOYEE):
            u = make_user(role)
            u.profile.consent_agreed = True
            u.profile.save()
            self.client.force_login(u)
            for name in PATIENT_URLS:
                self.assertEqual(self.client.get(reverse(name)).status_code, 200, f"{role} {name}")

    def test_staff_roles_cannot_open_patient_pages(self):
        for role in (Role.NURSE, Role.DOCTOR, Role.DENTIST, Role.VOLUNTEER, Role.ADMIN):
            self.client.force_login(make_user(role))
            for name in PATIENT_URLS:
                resp = self.client.get(reverse(name))
                if name == "core:dashboard":  # login lands here, then moves on to the staff page
                    self.assertRedirects(resp, reverse("core:staff_home"), fetch_redirect_response=False)
                else:
                    self.assertEqual(resp.status_code, 403, f"{role} {name}")

    def test_staff_toggle_is_forbidden(self):
        self.client.force_login(make_user(Role.NURSE))
        resp = self.client.post(reverse("accounts:toggle_setting"), {"setting": "sms_alerts"})
        self.assertEqual(resp.status_code, 403)

    def test_staff_home_only_for_staff(self):
        self.client.force_login(make_user(Role.DOCTOR))
        self.assertEqual(self.client.get(reverse("core:staff_home")).status_code, 200)
        self.client.force_login(make_student())
        self.assertEqual(self.client.get(reverse("core:staff_home")).status_code, 403)

    def test_anonymous_goes_to_login(self):
        resp = self.client.get(reverse("core:staff_home"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp["Location"])


class ConsentTests(TestCase):
    def setUp(self):
        self.user = make_student()
        self.user.profile.consent_agreed = False
        self.user.profile.save()
        self.client.force_login(self.user)
        self.url = reverse("accounts:consent")

    def test_patient_without_consent_is_sent_to_terms(self):
        for name in ("core:dashboard", "accounts:profile", "appointments:book", "accounts:export"):
            resp = self.client.get(reverse(name))
            self.assertEqual(resp.status_code, 302, name)
            self.assertTrue(resp["Location"].startswith(self.url), name)

    def test_post_requests_are_gated_too(self):
        resp = self.client.post(reverse("accounts:toggle_setting"), {"setting": "sms_alerts"})
        self.assertTrue(resp["Location"].startswith(self.url))

    def test_terms_page_and_logout_stay_reachable(self):
        self.assertContains(self.client.get(self.url), "Terms and data privacy consent")
        resp = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(resp, reverse("accounts:login"), fetch_redirect_response=False)

    def test_must_tick_the_box(self):
        resp = self.client.post(self.url, {})
        self.assertContains(resp, "Tick the box")
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.consent_agreed)

    def test_agreeing_records_consent_and_logs_it(self):
        resp = self.client.post(self.url, {"agree": "1", "next": reverse("accounts:profile")})
        self.assertRedirects(resp, reverse("accounts:profile"), fetch_redirect_response=False)
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.consent_agreed)
        self.assertIsNotNone(self.user.profile.consent_date)
        self.assertTrue(ActivityLog.objects.filter(user=self.user, action=activity.CONSENT).exists())
        self.assertEqual(self.client.get(reverse("accounts:profile")).status_code, 200)

    def test_next_cannot_leave_the_site(self):
        resp = self.client.post(self.url, {"agree": "1", "next": "https://evil.example/"})
        self.assertRedirects(resp, reverse("core:dashboard"), fetch_redirect_response=False)

    def test_already_consented_skips_terms(self):
        self.client.post(self.url, {"agree": "1"})
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_staff_are_not_gated(self):
        self.client.force_login(make_user(Role.NURSE))
        self.assertEqual(self.client.get(reverse("core:staff_home")).status_code, 200)

    def test_staff_cannot_open_terms(self):
        self.client.force_login(make_user(Role.NURSE))
        self.assertEqual(self.client.get(self.url).status_code, 403)


class SessionTimeoutTests(TestCase):
    def test_idle_length_comes_from_settings(self):
        from django.conf import settings
        self.assertEqual(settings.SESSION_COOKIE_AGE, settings.SESSION_IDLE_MINUTES * 60)
        self.assertTrue(settings.SESSION_SAVE_EVERY_REQUEST)  # expiry restarts on each request

    def test_expiry_refreshes_on_each_request(self):
        user = make_student()
        self.client.force_login(user)
        session = Session.objects.get()
        session.expire_date = timezone.now() + timedelta(seconds=30)
        session.save()
        self.client.get(reverse("core:dashboard"))
        self.assertGreater(Session.objects.get().expire_date, timezone.now() + timedelta(minutes=10))

    def test_expired_session_is_signed_out(self):
        self.client.force_login(make_student())
        Session.objects.update(expire_date=timezone.now() - timedelta(seconds=1))
        resp = self.client.get(reverse("core:dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("accounts:login"), resp["Location"])

    def test_login_page_explains_inactivity_logout(self):
        self.assertContains(self.client.get(reverse("accounts:login")), "signed out after 15 minutes of inactivity")


class ActivityLogTests(TestCase):
    def test_login_failed_login_and_logout_are_logged(self):
        user = make_student()
        self.client.post(reverse("accounts:login"), {"username": "sam", "password": "nope"})
        failed = ActivityLog.objects.get(action=activity.LOGIN_FAILED)
        self.assertIsNone(failed.user)
        self.assertEqual(failed.detail, "username=sam")
        self.assertNotIn("nope", failed.detail)
        self.client.post(reverse("accounts:login"), {"username": "sam", "password": "pw-12345-xyz"})
        self.assertTrue(ActivityLog.objects.filter(user=user, action=activity.LOGIN).exists())
        self.client.post(reverse("accounts:logout"))
        self.assertTrue(ActivityLog.objects.filter(user=user, action=activity.LOGOUT).exists())

    def test_log_activity_accepts_no_user(self):
        entry = activity.log_activity(None, "x", "mod", 7, "d")
        self.assertEqual((entry.user, entry.object_id), (None, "7"))

    def test_role_change_in_admin_is_logged(self):
        boss = User.objects.create_superuser("boss", password="pw-12345-xyz")
        target = make_student()
        self.client.force_login(boss)
        url = reverse("admin:accounts_user_change", args=[target.pk])
        data = {"username": "sam", "role": Role.NURSE, "first_name": "Sam", "last_name": "Cruz",
                "email": "", "is_active": "on", "date_joined_0": "2026-01-01", "date_joined_1": "00:00:00",
                # inline management forms
                "profile-TOTAL_FORMS": "0", "profile-INITIAL_FORMS": "0",
                "settings-TOTAL_FORMS": "0", "settings-INITIAL_FORMS": "0"}
        self.client.post(url, data)
        target.refresh_from_db()
        self.assertEqual(target.role, Role.NURSE)
        entry = ActivityLog.objects.get(action=activity.ROLE_CHANGED)
        self.assertEqual((entry.user, entry.object_id, entry.detail), (boss, str(target.pk), "student -> nurse"))


class VisitorPatientTests(TestCase):
    def test_visitor_needs_no_user(self):
        v = Patient.objects.create(patient_type="visitor", full_name="Jo Visitor")
        self.assertIsNone(v.user)
        self.assertEqual(v.display_name, "Jo Visitor")
        self.assertIn("Jo Visitor", str(v))

    def test_nameless_patient_without_user_is_rejected(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Patient.objects.create(patient_type="visitor")

    def test_account_holder_name_comes_from_user(self):
        self.assertEqual(make_student().profile.display_name, "Sam Cruz")

    def test_volunteer_agreement_defaults_to_pending(self):
        a = VolunteerAgreement.objects.create(user=make_user(Role.VOLUNTEER))
        self.assertEqual(a.status, "pending")


class AdminAccessTests(TestCase):
    def test_only_admin_role_and_superusers_open_admin(self):
        index = reverse("admin:index")
        for role in (Role.NURSE, Role.DOCTOR, Role.DENTIST, Role.VOLUNTEER, Role.STUDENT):
            u = make_user(role)
            u.is_staff = True  # even a mistakenly flagged staff user is refused
            u.save()
            self.client.force_login(u)
            self.assertEqual(self.client.get(index).status_code, 302, role)
        self.client.force_login(make_user(Role.ADMIN))
        self.assertEqual(self.client.get(index).status_code, 200)
        self.client.force_login(User.objects.create_superuser("su", password="x"))
        self.assertEqual(self.client.get(index).status_code, 200)

    def test_system_administrator_manages_accounts_but_not_patient_data(self):
        admin_user = make_user(Role.ADMIN)
        student = make_student()
        self.client.force_login(admin_user)
        page = self.client.get(reverse("admin:accounts_user_change", args=[student.pk]))
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "Health information")
        self.assertNotContains(page, "Allergies")
        self.assertEqual(self.client.get(reverse("admin:accounts_activitylog_changelist")).status_code, 200)

    def test_activity_log_cannot_be_edited_from_admin(self):
        self.client.force_login(User.objects.create_superuser("su", password="x"))
        self.assertEqual(self.client.get(reverse("admin:accounts_activitylog_add")).status_code, 403)

    def test_superuser_sees_patient_data(self):
        self.client.force_login(User.objects.create_superuser("su", password="x"))
        page = self.client.get(reverse("admin:accounts_user_change", args=[make_student().pk]))
        self.assertContains(page, "Health information")


class RenameMigrationTests(TransactionTestCase):
    """StudentProfile -> Patient must keep every existing row."""

    def test_existing_profiles_survive(self):
        executor = MigrationExecutor(connection)
        executor.migrate([("accounts", "0003_backfill_profiles")])
        old = executor.loader.project_state([("accounts", "0003_backfill_profiles")]).apps
        u = old.get_model("accounts", "User").objects.create(username="legacy", is_superuser=False)
        old.get_model("accounts", "StudentProfile").objects.update_or_create(
            user=u, defaults={"student_id": "2020-00001", "allergies": "Penicillin"}
        )
        su = old.get_model("accounts", "User").objects.create(username="rootlegacy", is_superuser=True)

        executor = MigrationExecutor(connection)
        executor.migrate(executor.loader.graph.leaf_nodes())
        new = executor.loader.project_state(executor.loader.graph.leaf_nodes()).apps
        patient = new.get_model("accounts", "Patient").objects.get(user__username="legacy")
        self.assertEqual((patient.student_id, patient.allergies), ("2020-00001", "Penicillin"))
        self.assertEqual(patient.patient_type, "student")
        self.assertFalse(patient.consent_agreed)
        self.assertEqual(new.get_model("accounts", "User").objects.get(pk=su.pk).role, "admin")
        self.assertFalse(new.get_model("accounts", "Patient").objects.filter(user_id=su.pk).exists())
