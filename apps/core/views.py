from django.views.generic import TemplateView

from apps.accounts.models import PATIENT_ROLES, STAFF_ROLES
from apps.accounts.permissions import RoleRequiredMixin

from . import mock
from .utils import safe_reverse


class DashboardView(RoleRequiredMixin, TemplateView):
    allowed_roles = PATIENT_ROLES + STAFF_ROLES

    def get_template_names(self):
        # Staff get the Figma clinic dashboard; patients keep the student one.
        return ["core/staff_dashboard.html" if self.request.user.role in STAFF_ROLES else "core/dashboard.html"]

    # (label, icon, url name or None when the page is not built yet)
    QUICK_ACTIONS = [
        ("Book Appointment", "lu-calendar-plus", "appointments:book"),
        ("View Queue", "lu-user-round", "appointments:queue"),
        ("View Health Record", "lu-circle-x", None),
        ("View Appointments", "lu-calendar-clock", "appointments:history"),
        ("View Certificates", "lu-award", None),
        ("View Prescriptions", "lu-bottle-wine", None),
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.role in STAFF_ROLES:
            ctx.update(mock.staff_overview())
            return ctx
        quick_actions = [
            {
                "label": label,
                "icon": icon,
                "href": safe_reverse(url) if url else "",
                "soon": not url,
                "variant": "gold" if i == 0 else "outline",
            }
            for i, (label, icon, url) in enumerate(self.QUICK_ACTIONS)
        ]
        ctx.update(
            appointment=mock.APPOINTMENT,
            schedule=mock.SCHEDULE,
            quick_actions=quick_actions,
            book_url=safe_reverse("appointments:book"),
            queue_url=safe_reverse("appointments:queue"),
            schedule_url=safe_reverse("appointments:schedule"),
        )
        return ctx


FAQS = [
    ("What is MediSync?", "A student clinic platform that turns booking into a live queue. You pick a practitioner and slot, answer a short triage questionnaire, and get a queue number plus SMS updates."),
    ("Does the triage replace a doctor?", "No. Triage is queue-priority support only, not a diagnosis. A clinician always reviews your answers before you are seen."),
    ("Can I cancel or reschedule?", "Yes. Free of charge up to 15 minutes before your slot. Open Queue Status and use Cancel, or rebook from the Dashboard."),
    ("Where is the clinic?", "Room 2, Ground Floor, Clinic Wing. Arrive 15 minutes early and tap the kiosk to activate your queue number."),
]


class HelpView(RoleRequiredMixin, TemplateView):
    template_name = "core/help.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["faqs"] = FAQS  # TEMPORARY: becomes the FAQ model in Stage 8
        ctx["queue_url"] = safe_reverse("appointments:queue")
        return ctx


class StaffHomeView(RoleRequiredMixin, TemplateView):
    """TEMPORARY landing for staff accounts until the Stage 8 portal replaces it."""

    template_name = "core/staff_home.html"
    allowed_roles = STAFF_ROLES
