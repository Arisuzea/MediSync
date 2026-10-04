"""Role checks. Every staff view uses one of these (PLAN section 6).

    class QueueDesk(RoleRequiredMixin, View):
        allowed_roles = (Role.NURSE,)

    @role_required(Role.STUDENT, Role.EMPLOYEE)
    def export_data(request): ...

Anonymous users go to the login page; signed-in users with the wrong role get 403.
"""

from functools import wraps

from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .models import PATIENT_ROLES


class RoleRequiredMixin(AccessMixin):
    allowed_roles = PATIENT_ROLES

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorator
