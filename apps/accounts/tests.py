from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import StudentProfile, UserSettings

User = get_user_model()


def make_student(username="sam", student_id="2024-00001", password="pw-12345-xyz"):
    user = User.objects.create_user(username, password=password, first_name="Sam", last_name="Cruz")
    user.profile.student_id = student_id
    user.profile.save()
    return user


class SignalTests(TestCase):
    def test_new_user_gets_profile_and_settings(self):
        u = User.objects.create_user("new", password="x")
        self.assertTrue(StudentProfile.objects.filter(user=u).exists())
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
