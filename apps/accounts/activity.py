from .models import ActivityLog

# Action names used across the project. Add new ones here so the log stays greppable.
LOGIN = "login"
LOGIN_FAILED = "login_failed"
LOGOUT = "logout"
CONSENT = "consent_given"
ROLE_CHANGED = "role_changed"


def log_activity(user, action, module="", object_id="", detail=""):
    """Record one audit event. `user` may be None (e.g. a failed login)."""
    return ActivityLog.objects.create(
        user=user if getattr(user, "pk", None) else None,
        action=action,
        module=module,
        object_id=str(object_id),
        detail=detail[:255],
    )
