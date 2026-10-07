"""Template context available on every page (sidebar, topbar)."""

from django.conf import settings
from django.urls import NoReverseMatch, reverse

from . import mock
from .navigation import MAIN_NAV, page_meta

# Pages that belong to the booking flow highlight "Dashboard" in the prototype
# only for priority/confirmation; we keep that behaviour here.
_DASHBOARD_ALSO = {"appointments:result", "appointments:confirmation"}


def _resolve(items, current):
    resolved = []
    for item in items:
        try:
            href = reverse(item["url"]) if item["url"] else ""
        except NoReverseMatch:
            href = ""  # page not built yet -> sidebar shows it inert
        active = current == item["url"] or (
            item["url"] == "core:dashboard" and current in _DASHBOARD_ALSO
        )
        resolved.append({**item, "href": href, "active": active})
    return resolved


def _student(user):
    p = user.profile
    return {
        "name": user.display_name,
        "first_name": user.first_display_name,
        "student_id": p.student_id or "",
        "course": p.course,
    }


def layout(request):
    match = request.resolver_match
    if match and match.namespace:
        current = f"{match.namespace}:{match.url_name}"
    else:
        current = match.url_name if match else ""
    ctx = {"page_meta": page_meta(current), "idle_minutes": settings.SESSION_IDLE_MINUTES}
    if not (request.user.is_authenticated and request.user.is_patient_role):
        return ctx  # staff pages (Stage 8) bring their own shell
    ctx.update(
        main_nav=_resolve(MAIN_NAV, current),
        student=_student(request.user),
        # TEMPORARY (Stages 3-8 replace these with real data):
        notifications=mock.NOTIFICATIONS,
        unread_count=sum(1 for n in mock.NOTIFICATIONS if n["unread"]),
        active_appointment=mock.APPOINTMENT,
        queue=mock.queue_summary(mock.APPOINTMENT),
    )
    return ctx
