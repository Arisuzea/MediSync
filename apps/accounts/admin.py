from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .activity import ROLE_CHANGED, log_activity
from .models import ActivityLog, Patient, Role, User, UserSettings, VolunteerAgreement


def _admin_site_access(request):
    """Only the System Administrator role and superusers may open /admin/ (FR-12)."""
    u = request.user
    return u.is_active and u.is_staff and (u.is_superuser or u.role == Role.ADMIN)


admin.site.has_permission = _admin_site_access


class PatientInline(admin.StackedInline):
    model = Patient
    can_delete = False
    fieldsets = (
        (None, {"fields": ("patient_type", "student_id", "course", "year_level", "phone")}),
        ("Health information", {"fields": ("blood_type", "allergies", "notes")}),
        ("Emergency contact", {"fields": ("emergency_name", "emergency_relationship", "emergency_phone")}),
    )


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False


@admin.register(User)
class MediSyncUserAdmin(UserAdmin):
    inlines = [PatientInline, UserSettingsInline]
    list_display = ("username", "get_full_name", "email", "role", "student_id", "is_staff")
    list_filter = ("role", "is_active", "is_staff", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email", "profile__student_id")
    fieldsets = UserAdmin.fieldsets + (("Clinic role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Clinic role", {"fields": ("role",)}),)

    def get_inlines(self, request, obj):
        # The System Administrator manages accounts but never sees patient health data.
        return self.inlines if request.user.is_superuser else [UserSettingsInline]

    @admin.display(description="Student ID", ordering="profile__student_id")
    def student_id(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.student_id if profile else ""

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and "role" in form.changed_data:
            log_activity(request.user, ROLE_CHANGED, "accounts", obj.pk,
                         f"{form.initial.get('role')} -> {obj.role}")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action", "module", "object_id", "detail")
    list_filter = ("action", "module")
    search_fields = ("user__username", "detail", "object_id")
    date_hierarchy = "created_at"

    # Append-only: nobody edits or deletes the audit trail from the admin.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(VolunteerAgreement)
class VolunteerAgreementAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "signed_at")
    list_filter = ("status",)
