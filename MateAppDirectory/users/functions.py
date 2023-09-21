from django.conf import settings
from django.contrib.auth import get_user_model

def checkUserActivationLimit(muser):
    activeUsers = get_user_model().objects.filter(is_active=True).exclude(is_superuser=True).count()
    if activeUsers >= int(settings.USER_LIMIT) and not muser.is_active:
        return False
    else:
        return True

def checkUserCreationLimit():
    activeUsers = get_user_model().objects.filter(is_active=True).exclude(is_superuser=True).count()
    if activeUsers >= int(settings.USER_LIMIT):
        return False
    else:
        return True