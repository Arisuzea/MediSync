"""TEMPORARY prototype data so the layout shell has something to show.

Everything here is replaced by real models in later stages:
    STUDENT       -> accounts.Patient   (Stage 2)
    NOTIFICATIONS -> notifications.Notification (Stage 8)
    APPOINTMENT   -> appointments.Appointment   (Stage 6)
    RECENT        -> Appointment history query  (Stage 8)
    SCHEDULE      -> practitioner availability (Stage 4)
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
    {"title": "Appointment Confirmed via SMS", "body": "Your dental reservation with Dr. Benson has been logged on the system.", "when": "2h ago", "unread": True},
    {"title": "Queue Position Updated", "body": "Patient #46 served. Estimated wait time is down to 12 minutes.", "when": "10m ago", "unread": True},
    {"title": "New Prescription Available", "body": "Dr. Reyes generated digital prescription cert for Amoxicillin.", "when": "Yesterday", "unread": True},
]

APPOINTMENT = {
    "practitioner": "Dr. Juan Reyes",
    "role": "General Physician",
    "date": date(2026, 9, 25),
    "time": time(10, 0),
    "reason": "General Medicine Consultation",
    "service": "General Medicine",
    "priority": "MEDIUM",
    "queue_number": 52,
    "ahead": 5,
    "room": "Room 3",
    "called": True,
}

RECENT = [
    {"reason": "Fever / flu symptoms", "practitioner": "Dr. Marcus Tan", "date": date(2026, 9, 18), "priority": "MEDIUM", "status": "Completed"},
    {"reason": "Tooth cleaning", "practitioner": "Dr. Sofia Lim", "date": date(2026, 8, 5), "priority": "LOW", "status": "Completed"},
    {"reason": "Skin rash", "practitioner": "Dr. Elena Reyes", "date": date(2026, 7, 22), "priority": "LOW", "status": "Cancelled"},
]

SCHEDULE = [
    {"name": "Dr. Juan Reyes", "department": "General Medicine", "hours": "Mon - Wed, 9:00 AM - 12:00 PM", "next": "Available Today"},
    {"name": "Dr. Clara Benson", "department": "Dental Service", "hours": "Tue & Thu, 1:00 PM - 4:00 PM", "next": "Slots Tomorrow"},
    {"name": "Dr. Gabriel Santos", "department": "General Medicine", "hours": "Fri, 8:30 AM - 11:30 AM", "next": "Available today"},
]

_WAITS = {"HIGH": "~5 Mins", "MEDIUM": "~15 Mins", "LOW": "~45 Mins"}


def queue_summary(appointment):
    """Derived queue numbers (the prototype's wait() / serving calculations)."""
    if not appointment:
        return None
    ahead = appointment["ahead"]
    serving = max(1, appointment["queue_number"] - ahead)
    return {
        "serving": serving,
        "next_up": serving + 1,
        "ahead": ahead,
        "wait": _WAITS[appointment["priority"]],
        "progress": round(serving / appointment["queue_number"] * 100),
        "called": appointment.get("called", False),
    }


# Staff screens (Figma 03 Clinic dashboard, 06 Queue management). Sample data, fictional.
STAFF_QUEUE = [
    {"no": "Q-021", "name": "Rafael Garcia", "type": "Student", "symptoms": "Fatigue", "priority": "Medium", "status": "Waiting"},
    {"no": "Q-022", "name": "Joshua Luis Mendoza", "type": "Student", "symptoms": "Minor scrape", "priority": "High", "status": "Waiting"},
    {"no": "Q-023", "name": "Andrea Mae Dela Cruz", "type": "Student", "symptoms": "Headache", "priority": "Low", "status": "In consultation"},
    {"no": "Q-024", "name": "Paolo Miguel Santos", "type": "Staff", "symptoms": "Stomach discomfort", "priority": "Medium", "status": "Waiting"},
    {"no": "Q-025", "name": "Mariel Bautista", "type": "Student", "symptoms": "Sore throat", "priority": "Low", "status": "Waiting"},
    {"no": "Q-020", "name": "Camille Reyes", "type": "Student", "symptoms": "Dizziness", "priority": "Low", "status": "Completed"},
]

STAFF_APPOINTMENTS = [
    {"time": "10:00 AM", "name": "Rafael Garcia", "service": "General consultation"},
    {"time": "11:00 AM", "name": "Paolo Miguel Santos", "service": "Dental review"},
    {"time": "02:00 PM", "name": "Andrea Mae Dela Cruz", "service": "General consultation"},
]


def staff_overview():
    q = STAFF_QUEUE
    count = lambda key, val: sum(1 for r in q if r[key] == val)  # noqa: E731
    return {
        "queue_rows": q,
        "waiting_rows": [r for r in q if r["status"] == "Waiting"],
        "staff_appointments": STAFF_APPOINTMENTS,
        "n_patients": len(q),
        "n_students": count("type", "Student"),
        "n_staff": count("type", "Staff"),
        "n_waiting": count("status", "Waiting"),
        "n_consult": count("status", "In consultation"),
        "n_done": count("status", "Completed"),
        "n_done_share": round(count("status", "Completed") / len(q) * 100, 3),
    }
