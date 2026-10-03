from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom user. Empty for now, but swapping the user model later is painful."""
    pass