"""Toast helper. The prototype's toast(kind, title, body) becomes Django messages.

A message is stored as "Title\nBody"; the toasts partial splits it back apart
with the `toast_title` / `toast_body` filters.
"""

from django.contrib import messages

_LEVELS = {
    "success": messages.SUCCESS,
    "info": messages.INFO,
    "warning": messages.WARNING,
    "error": messages.ERROR,
}


def toast(request, kind, title, body=""):
    messages.add_message(request, _LEVELS[kind], f"{title}\n{body}" if body else title)
