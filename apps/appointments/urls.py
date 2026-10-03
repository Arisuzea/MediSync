from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("book/", views.BookView.as_view(), name="book"),
    path("book/practitioner/", views.PractitionerView.as_view(), name="practitioner"),
    path("book/schedule/", views.ScheduleView.as_view(), name="schedule"),
    path("book/symptoms/", views.SymptomsView.as_view(), name="symptoms"),
    path("book/result/", views.ResultView.as_view(), name="result"),
    path("appointments/confirmation/", views.ConfirmationView.as_view(), name="confirmation"),
    path("queue/", views.QueueView.as_view(), name="queue"),
    path("history/", views.HistoryView.as_view(), name="history"),
]
