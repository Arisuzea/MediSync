from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("staff/", views.StaffHomeView.as_view(), name="staff_home"),
    path("help/", views.HelpView.as_view(), name="help"),
]
