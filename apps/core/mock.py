"""TEMPORARY prototype data so the layout shell has something to show.

Everything here is replaced by real models in later stages:
    STUDENT       -> accounts.Patient   (Stage 2)
    NOTIFICATIONS -> notifications.Notification (Stage 8)
    APPOINTMENT   -> appointments.Appointment   (Stage 6)
    RECENT        -> Appointment history query  (Stage 8)
Delete this file once nothing imports it.
"""

from datetime import date, time

STUDENT = {
    "name": "Alex Mendoza",
    "first_name": "Alex",
    "student_id": "2023-11482",
    "course": "BS Computer Science",
}

NOTIFICATIONS = [
    {"title": "Appointment confirmed", "body": "Dr. Elena Reyes · Oct 6 at 9:30 AM · Queue #14", "when": "2h ago", "unread": True},
    {"title": "Queue update", "body": "You are 3 places away from being called.", "when": "10m ago", "unread": True},
    {"title": "Bring your student ID", "body": "Required at clinic check-in.", "when": "Yesterday", "unread": False},
]

APPOINTMENT = {
    "practitioner": "Dr. Elena Reyes",
    "role": "General Physician",
    "date": date(2026, 10, 6),
    "time": time(9, 30),
    "reason": "General check-up",
    "priority": "MEDIUM",
    "queue_number": 14,
    "ahead": 3,
    "room": "Room 2",
}

RECENT = [
    {"reason": "Fever / flu symptoms", "practitioner": "Dr. Marcus Tan", "date": date(2026, 9, 18), "priority": "MEDIUM", "status": "Completed"},
    {"reason": "Tooth cleaning", "practitioner": "Dr. Sofia Lim", "date": date(2026, 8, 5), "priority": "LOW", "status": "Completed"},
    {"reason": "Skin rash", "practitioner": "Dr. Elena Reyes", "date": date(2026, 7, 22), "priority": "LOW", "status": "Cancelled"},
]

_WAITS = {"HIGH": "5–10 min", "MEDIUM": "20–30 min", "LOW": "45–60 min"}


def queue_summary(appointment):
    """Derived queue numbers (the prototype's wait() / serving calculations)."""
    if not appointment:
        return None
    ahead = appointment["ahead"]
    return {
        "serving": max(1, appointment["queue_number"] - ahead),
        "ahead": ahead,
        "wait": _WAITS[appointment["priority"]],
    }
