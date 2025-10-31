from django.contrib.auth.views import redirect_to_login
from django_auth_adfs.exceptions import MFARequired

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware requires authentication middleware to be installed. Edit your MIDDLEWARE setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'. If that doesn't work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes 'django.core.context_processors.auth'."
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any((m.match(path) for m in LOGIN_EXEMPT_URLS)):
                try:
                    return redirect_to_login(request.get_full_path())
                except MFARequired:
                    return redirect_to_login('django_auth_adfs:login-force-mfa')
        return self.get_response(request)