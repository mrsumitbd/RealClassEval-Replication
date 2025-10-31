from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import get_object_or_404, resolve_url

class SuccessUrlMixin:
    redirect_field_name = 'next'
    success_url = '/'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(self.success_url or '/')

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(self.redirect_field_name, self.request.GET.get(self.redirect_field_name, ''))
        url_is_safe = url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts=self.request.get_host(), require_https=self.request.is_secure())
        return redirect_to if url_is_safe else ''