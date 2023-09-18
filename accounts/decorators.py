from django.shortcuts import redirect
from django.conf import settings

def user_not_authenticated(function=None, redirect_url='home'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if 'remember_me' in request.POST and request.POST['remember_me']:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    if function:
        return decorator(function)
    return decorator
