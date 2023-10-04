from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test


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


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) and not u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='403')

def admin_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) and u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='403')
