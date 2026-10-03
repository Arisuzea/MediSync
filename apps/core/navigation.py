"""Sidebar structure and page titles/breadcrumbs, kept out of templates.

`url` is a URL *name*. Entries whose URL doesn't exist yet (later stages) are
rendered as disabled links by the sidebar template, so the shell works today.
"""

MAIN_NAV = [
    {"label": "Dashboard", "icon": "dashboard", "url": "core:dashboard"},
    {"label": "Book Appointment", "icon": "calplus", "url": "appointments:book"},
    {"label": "Queue Status", "icon": "list", "url": "appointments:queue"},
    {"label": "Visit History", "icon": "history", "url": "appointments:history"},
    {"label": "Medical Profile", "icon": "user", "url": "accounts:profile"},
    {"label": "Settings", "icon": "settings", "url": "accounts:settings"},
]

SUPPORT_NAV = [
    {"label": "Help & Support", "icon": "help", "url": "core:help"},
]

# url name -> (title, breadcrumb)  — from the prototype's META object
PAGE_META = {
    "core:dashboard": ("Dashboard", "Home / Overview"),
    "appointments:book": ("Book Appointment", "Appointments / New"),
    "appointments:practitioner": ("Select Practitioner", "Appointments / New / Practitioner"),
    "appointments:schedule": ("View Schedule", "Appointments / New / Schedule"),
    "appointments:symptoms": ("Symptom Questionnaire", "Appointments / New / Triage"),
    "appointments:result": ("Priority Result", "Appointments / New / Triage Result"),
    "appointments:confirmation": ("Appointment Confirmation", "Appointments / Confirmed"),
    "appointments:queue": ("Queue Status", "Live / Queue"),
    "appointments:history": ("Visit History", "Records"),
    "accounts:profile": ("Medical Profile", "Account / Profile"),
    "accounts:settings": ("Settings", "Account / Settings"),
    "core:help": ("Help & Support", "Support"),
}


def page_meta(current):
    title, crumb = PAGE_META.get(current, ("MediSync", ""))
    return {"title": title, "crumb": crumb}
