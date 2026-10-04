import json

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.decorators.http import require_POST

from apps.core.messaging import toast

from . import activity
from .forms import EmergencyContactForm, LoginForm, ProfileForm
from .models import PATIENT_ROLES, UserSettings
from .permissions import RoleRequiredMixin, role_required

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


class ProfileView(RoleRequiredMixin, View):
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


class EmergencyContactView(RoleRequiredMixin, View):
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


class SettingsView(RoleRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/settings.html", {"s": request.user.settings})


@require_POST
@role_required(*PATIENT_ROLES)
def toggle_setting(request):
    """One switch = one tiny form. Server flips the boolean; no JS required."""
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


class StudentPasswordChangeView(RoleRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:settings")

    def form_valid(self, form):
        response = super().form_valid(form)
        toast(self.request, "success", "Password changed", "Use your new password next time you sign in.")
        return response


@role_required(*PATIENT_ROLES)
def export_data(request):
    """'Download my data': the student's own profile and settings as JSON.

    Later stages add appointments and notifications to this payload.
    """
    u, p, s = request.user, request.user.profile, request.user.settings
    payload = {
        "exported_at": timezone.localtime().isoformat(timespec="seconds"),
        "account": {"username": u.username, "name": u.get_full_name(), "email": u.email},
        "profile": {
            "patient_type": p.patient_type, "birth_date": p.birth_date and p.birth_date.isoformat(),
            "sex": p.sex, "address": p.address,
            "guardian_name": p.guardian_name, "guardian_phone": p.guardian_phone,
            "consent_agreed": p.consent_agreed,
            "consent_date": p.consent_date and p.consent_date.isoformat(timespec="seconds"),
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


class ConsentView(RoleRequiredMixin, View):
    """Terms and data-privacy consent. The middleware sends patients here until they agree."""

    template_name = "accounts/consent.html"

    def _next(self, request):
        target = request.POST.get("next") or request.GET.get("next") or ""
        ok = url_has_allowed_host_and_scheme(target, {request.get_host()}, request.is_secure())
        return target if ok else reverse_lazy("core:dashboard")

    def get(self, request):
        if request.user.profile.consent_agreed:
            return redirect(self._next(request))
        return render(request, self.template_name, {"next": self._next(request)})

    def post(self, request):
        if not request.POST.get("agree"):
            ctx = {"next": self._next(request), "error": "Tick the box to agree before you continue."}
            return render(request, self.template_name, ctx)
        patient = request.user.profile
        patient.consent_agreed = True
        patient.consent_date = timezone.now()
        patient.save(update_fields=["consent_agreed", "consent_date"])
        activity.log_activity(request.user, activity.CONSENT, "accounts", patient.pk)
        toast(request, "success", "Thank you", "Your consent is recorded.")
        return redirect(self._next(request))
