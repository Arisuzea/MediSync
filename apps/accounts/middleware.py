from django.shortcuts import redirect
from django.urls import reverse

CONSENT_EXEMPT = {"accounts:consent", "accounts:logout"}


class ConsentRequiredMiddleware:
    """Signed-in patients who have not agreed to the terms can only see the terms page
    and sign out (FR-13). Staff accounts are not patients and pass through."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        if not (user.is_authenticated and user.is_patient_role):
            return None
        match = request.resolver_match
        if f"{match.namespace}:{match.url_name}" in CONSENT_EXEMPT or user.profile.consent_agreed:
            return None
        return redirect(f"{reverse('accounts:consent')}?next={request.get_full_path()}")
