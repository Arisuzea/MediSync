from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import mock
from .utils import safe_reverse


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tiles = [
            {"icon": "calplus", "label": "Book Appointment", "hint": "Doctor or dentist, in 60 seconds", "url": "appointments:book", "tone": ""},
            {"icon": "list", "label": "View Queue", "hint": "Live position & wait estimate", "url": "appointments:queue", "tone": "nv"},
            {"icon": "history", "label": "Visit History", "hint": "Records, notes & follow-ups", "url": "appointments:history", "tone": "nv"},
            {"icon": "user", "label": "Medical Profile", "hint": "Allergies, blood type, contacts", "url": "accounts:profile", "tone": ""},
        ]
        for t in tiles:
            t["href"] = safe_reverse(t["url"])
        ctx.update(
            appointment=mock.APPOINTMENT,
            recent=mock.RECENT,
            tiles=tiles,
            book_url=safe_reverse("appointments:book"),
            queue_url=safe_reverse("appointments:queue"),
            confirmation_url=safe_reverse("appointments:confirmation"),
            schedule_url=safe_reverse("appointments:schedule"),
            history_url=safe_reverse("appointments:history"),
            help_url=safe_reverse("core:help"),
        )
        return ctx


FAQS = [
    ("What is MediSync?", "A student clinic platform that turns booking into a live queue. You pick a practitioner and slot, answer a short triage questionnaire, and get a queue number plus SMS updates."),
    ("Does the triage replace a doctor?", "No. Triage is queue-priority support only, not a diagnosis. A clinician always reviews your answers before you are seen."),
    ("Can I cancel or reschedule?", "Yes. Free of charge up to 15 minutes before your slot. Open Queue Status and use Cancel, or rebook from the Dashboard."),
    ("Where is the clinic?", "Room 2, Ground Floor, Clinic Wing. Arrive 15 minutes early and tap the kiosk to activate your queue number."),
]


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = "core/help.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faqs"] = FAQS  # TEMPORARY: becomes the FAQ model in Stage 8
        ctx["queue_url"] = safe_reverse("appointments:queue")
        return ctx
