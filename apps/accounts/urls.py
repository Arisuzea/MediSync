from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("accounts/login/", views.StudentLoginView.as_view(), name="login"),
    path("accounts/logout/", views.StudentLogoutView.as_view(), name="logout"),
    path("accounts/password/", views.StudentPasswordChangeView.as_view(), name="password_change"),
    path("consent/", views.ConsentView.as_view(), name="consent"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/emergency/", views.EmergencyContactView.as_view(), name="emergency_contact"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("settings/toggle/", views.toggle_setting, name="toggle_setting"),
    path("export/", views.export_data, name="export"),
]
