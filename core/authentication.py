from django.contrib.auth.backends import ModelBackend
from .models import Resident

class BlacklistAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and Resident.objects.filter(user=user, is_blacklisted=True).exists():
            return None  # User is blacklisted, don't authenticate
        return user