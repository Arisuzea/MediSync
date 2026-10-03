"""Template context available on every page (sidebar, topbar)."""

from django.urls import NoReverseMatch, reverse

from . import mock
from .navigation import MAIN_NAV, SUPPORT_NAV, page_meta

# Pages that belong to the booking flow highlight "Dashboard" in the prototype
# only for priority/confirmation; we keep that behaviour here.
_DASHBOARD_ALSO = {"appointments:result", "appointments:confirmation"}


def _resolve(items, current):
    resolved = []
    for item in items:
        try:
            href = reverse(item["url"])
        except NoReverseMatch:
            href = ""  # page not built yet -> sidebar shows it disabled
        active = current == item["url"] or (
            item["url"] == "core:dashboard" and current in _DASHBOARD_ALSO
        )
        resolved.append({**item, "href": href, "active": active})
    return resolved


def layout(request):
    match = request.resolver_match
    if match and match.namespace:
        current = f"{match.namespace}:{match.url_name}"
    else:
        current = match.url_name if match else ""
    return {
        "main_nav": _resolve(MAIN_NAV, current),
        "support_nav": _resolve(SUPPORT_NAV, current),
        "page_meta": page_meta(current),
        # TEMPORARY (Stages 2-8 replace these with real data):
        "student": mock.STUDENT,
        "notifications": mock.NOTIFICATIONS,
        "unread_count": sum(1 for n in mock.NOTIFICATIONS if n["unread"]),
        "active_appointment": mock.APPOINTMENT,
        "queue": mock.queue_summary(mock.APPOINTMENT),
    }
