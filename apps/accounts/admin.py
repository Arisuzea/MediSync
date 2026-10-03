from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StudentProfile, User, UserSettings


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    fieldsets = (
        (None, {"fields": ("student_id", "course", "year_level", "phone")}),
        ("Health information", {"fields": ("blood_type", "allergies", "notes")}),
        ("Emergency contact", {"fields": ("emergency_name", "emergency_relationship", "emergency_phone")}),
    )


class UserSettingsInline(admin.StackedInline):
    model = UserSettings
    can_delete = False


@admin.register(User)
class MediSyncUserAdmin(UserAdmin):
    inlines = [StudentProfileInline, UserSettingsInline]
    list_display = ("username", "get_full_name", "email", "student_id", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email", "profile__student_id")

    @admin.display(description="Student ID", ordering="profile__student_id")
    def student_id(self, obj):
        return obj.profile.student_id

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")
