from django.conf import settings
from django.db.models import Q
from .models import User

# from django.contrib import messages


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user.email)
        user_email = user.email

        avatar = User.objects.filter(Q(email=user_email)).first()

        context = {
            "avatar": avatar,
        }
        return context
    # messages.error(request, "NotLoggedIn")
    return {"NotLoggedIn": User.objects.none()}
