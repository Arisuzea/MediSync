from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from apps.core.icons import ICONS

register = template.Library()


@register.simple_tag
def icon(name, size=18):
    """Render an inline SVG icon: {% icon "bell" 18 %}

    Falls back to the "info" icon for unknown names (same as the prototype).
    The path data comes from our own icons.py, so it is safe to mark as HTML.
    """
    paths = mark_safe(ICONS.get(name, ICONS["info"]))
    return format_html(
        '<svg width="{0}" height="{0}" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">{1}</svg>',
        size,
        paths,
    )


@register.filter
def initials(full_name):
    """'Dr. Elena Reyes' -> 'ER'."""
    parts = str(full_name).replace("Dr. ", "").split()
    if not parts:
        return "?"
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()


@register.simple_tag
def safe_url(name):
    """{% safe_url "appointments:book" as book_url %} -> "#" until that page exists."""
    from apps.core.utils import safe_reverse

    return safe_reverse(name)


@register.filter
def priority_tone(level):
    """HIGH/MEDIUM/LOW -> the badge colour suffix used in components.css."""
    return {"HIGH": "high", "MEDIUM": "med", "LOW": "low"}.get(level, "low")
