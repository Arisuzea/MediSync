"""TEMPORARY placeholder pages so every sidebar tab opens.

Each view shows prototype demo data from apps/core/mock.py. Stages 4-8 replace
them one by one with real views backed by Appointment, queue and history queries.
"""

from django.views.generic import TemplateView

from apps.accounts.permissions import RoleRequiredMixin
from apps.core import mock


class PlaceholderView(RoleRequiredMixin, TemplateView):
    template_name = "appointments/coming_soon.html"
    heading = ""
    blurb = ""
    stage = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(heading=self.heading, blurb=self.blurb, stage=self.stage)
        return ctx


class BookView(PlaceholderView):
    heading = "Book an appointment"
    blurb = "Choose a visit type, practitioner and time slot. The full booking flow arrives in Stage 4."
    stage = "Stage 4"


class PractitionerView(PlaceholderView):
    heading = "Select practitioner"
    blurb = "Pick a doctor or dentist. Arrives in Stage 4."
    stage = "Stage 4"


class ScheduleView(PlaceholderView):
    heading = "View schedule"
    blurb = "Calendar and time slots generated from practitioner availability. Arrives in Stage 4."
    stage = "Stage 4"


class SymptomsView(PlaceholderView):
    heading = "Symptom questionnaire"
    blurb = "Triage questions that decide your queue priority. Arrives in Stage 5."
    stage = "Stage 5"


class ResultView(PlaceholderView):
    heading = "Priority result"
    blurb = "Your estimated wait and queue position. Arrives in Stage 5."
    stage = "Stage 5"


class ConfirmationView(PlaceholderView):
    heading = "Appointment confirmation"
    blurb = "Your booking summary. Arrives in Stage 6."
    stage = "Stage 6"


class QueueView(RoleRequiredMixin, TemplateView):
    template_name = "appointments/queue.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["appt"] = mock.APPOINTMENT
        ctx["q"] = mock.queue_summary(mock.APPOINTMENT)
        return ctx


class HistoryView(RoleRequiredMixin, TemplateView):
    template_name = "appointments/history.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["rows"] = mock.RECENT
        return ctx
