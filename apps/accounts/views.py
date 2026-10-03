import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_POST

from apps.core.messaging import toast

from .forms import EmergencyContactForm, LoginForm, ProfileForm
from .models import UserSettings

SETTING_LABELS = {
    "sms_alerts": "SMS alerts",
    "email_reminders": "Email reminders",
    "queue_sound": "Queue sound",
    "auto_triage": "Auto-start triage",
    "share_anon_stats": "Share anonymous queue stats",
}


class StudentLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        toast(self.request, "success", "Welcome back", f"You’re signed in as {form.get_user().display_name}.")
        return response


class StudentLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        toast(request, "info", "Signed out", "Your booking is saved.")
        return response


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def _context(self, request, form, emergency_form=None, open_emergency=False):
        return {
            "form": form,
            "emergency_form": emergency_form or EmergencyContactForm(instance=request.user.profile),
            "open_emergency": open_emergency,
            "profile": request.user.profile,
        }

    def get(self, request):
        form = ProfileForm(instance=request.user.profile, user=request.user)
        return render(request, self.template_name, self._context(request, form))

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            toast(request, "success", "Profile saved", "Your clinic record is up to date.")
            return redirect("accounts:profile")
        toast(request, "error", "Profile not saved", "Fix the highlighted fields and try again.")
        return render(request, self.template_name, self._context(request, form))


class EmergencyContactView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        form = EmergencyContactForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            toast(request, "success", "Emergency contact saved")
            return redirect("accounts:profile")
        profile_form = ProfileForm(instance=request.user.profile, user=request.user)
        ctx = {
            "form": profile_form,
            "emergency_form": form,
            "open_emergency": True,
            "profile": request.user.profile,
        }
        return render(request, ProfileView.template_name, ctx, status=400)


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/settings.html", {"s": request.user.settings})


@require_POST
def toggle_setting(request):
    """One switch = one tiny form. Server flips the boolean; no JS required."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse_lazy('accounts:login')}?next={reverse_lazy('accounts:settings')}")
    key = request.POST.get("setting")
    if key not in UserSettings.TOGGLE_FIELDS:
        toast(request, "error", "Unknown setting")
        return redirect("accounts:settings")
    s = request.user.settings
    setattr(s, key, not getattr(s, key))
    s.save(update_fields=[key])
    state = "Enabled" if getattr(s, key) else "Disabled"
    toast(request, "info", "Setting updated", f"{state}: {SETTING_LABELS[key]}")
    return redirect("accounts:settings")


class StudentPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:settings")

    def form_valid(self, form):
        response = super().form_valid(form)
        toast(self.request, "success", "Password changed", "Use your new password next time you sign in.")
        return response


def export_data(request):
    """'Download my data': the student's own profile and settings as JSON.

    Later stages add appointments and notifications to this payload.
    """
    if not request.user.is_authenticated:
        return redirect(f"{reverse_lazy('accounts:login')}?next={reverse_lazy('accounts:export')}")
    u, p, s = request.user, request.user.profile, request.user.settings
    payload = {
        "exported_at": timezone.localtime().isoformat(timespec="seconds"),
        "account": {"username": u.username, "name": u.get_full_name(), "email": u.email},
        "profile": {
            "student_id": p.student_id, "course": p.course, "year_level": p.year_level,
            "phone": p.phone, "blood_type": p.blood_type, "allergies": p.allergies,
            "notes": p.notes,
            "emergency_contact": {
                "name": p.emergency_name, "relationship": p.emergency_relationship,
                "phone": p.emergency_phone,
            },
        },
        "settings": {f: getattr(s, f) for f in UserSettings.TOGGLE_FIELDS},
    }
    resp = HttpResponse(json.dumps(payload, indent=2), content_type="application/json")
    resp["Content-Disposition"] = 'attachment; filename="medisync-my-data.json"'
    return resp
