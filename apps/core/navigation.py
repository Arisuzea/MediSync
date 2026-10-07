"""Sidebar structure and page titles/breadcrumbs, kept out of templates.

`url` is a URL *name*. Entries whose URL doesn't exist yet (later stages) are
rendered as disabled links by the sidebar template, so the shell works today.
"""

# Order and labels follow the Figma sidebar. `url` is None for pages that do not exist
# yet; the sidebar shows those exactly like the mockup but inert (tooltip: coming later).
MAIN_NAV = [
    {"label": "Dashboard", "icon": "lu-layout-dashboard", "url": "core:dashboard"},
    {"label": "Book Appointment", "icon": "lu-calendar-plus", "url": "appointments:book"},
    {"label": "Queue Status", "icon": "lu-user-round", "url": "appointments:queue"},
    {"label": "Health Record", "icon": "lu-circle-x", "url": None},
    {"label": "Appointments", "icon": "lu-calendar-clock", "url": "appointments:history"},
    {"label": "Certificates", "icon": "lu-award", "url": None},
    {"label": "Prescriptions", "icon": "lu-bottle-wine", "url": None},
    {"label": "Notifications", "icon": "lu-bell-ring", "url": None, "badge": "unread"},
    {"label": "Profile", "icon": "lu-user-circle", "url": "accounts:profile"},
]

# url name -> (title, breadcrumb)  — from the prototype's META object
PAGE_META = {
    "core:dashboard": ("Dashboard Overview", "Home / Overview"),
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
