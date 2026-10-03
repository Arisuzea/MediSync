from django.views.generic import TemplateView

from . import mock
from .utils import safe_reverse


class DashboardView(TemplateView):
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
