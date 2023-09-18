from social_core.pipeline import user
from .models import CustomUser
from django.contrib import messages
from django.shortcuts import redirect

def check_email_exists(request, backend, details, uid, user=None, *args, **kwargs):
    email = details.get('email')
    provider = backend.name

    # check if social user exists to allow logging in (not sure if this is necessary)
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    # check if given email is in use
    count = CustomUser.objects.filter(username=email).count()

    if not user and not social and count:
        messages.error(request, 'Sorry, a user with that email already exists.')
        return redirect('')  # Change 'accounts:sign_up' to the appropriate URL name

    return None
