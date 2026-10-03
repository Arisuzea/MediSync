from django.urls import NoReverseMatch, reverse


def safe_reverse(name, default="#"):
    """reverse() that returns `default` instead of raising when a page isn't built yet.

    Only needed while we build the app stage by stage; once every URL exists
    we can switch templates to the plain {% url %} tag.
    """
    try:
        return reverse(name)
    except NoReverseMatch:
        return default
