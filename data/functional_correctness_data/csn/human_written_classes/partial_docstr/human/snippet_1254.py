from django.utils import timezone
import json
from django.conf import settings
import datetime

class AnalyticsPolicy:
    """
    Determines whether Google Analytics is enabled.
    Apps can require analytics or allow users to choose (by setting a long-lived cookie).
    """
    cookie_name = 'cookie_policy'

    def __init__(self, request):
        analytics_required = getattr(settings, 'ANALYTICS_REQUIRED', True)
        self.ga4_measurement_id = getattr(settings, 'GA4_MEASUREMENT_ID', None)
        self.ga4_enabled = self.ga4_measurement_id and (analytics_required or self.is_cookie_policy_accepted(request))

    def is_cookie_policy_accepted(self, request):
        """
        Checks for cookie policy being accepted in a cookie.
        Lack of cookie policy indicates that analytics should NOT enabled.
        """
        cookie_policy = request.COOKIES.get(self.cookie_name, '')
        try:
            cookie_policy = json.loads(cookie_policy)
            return isinstance(cookie_policy, dict) and cookie_policy.get('usage') is True
        except ValueError:
            return False

    def set_cookie_policy(self, response, accepted: bool):
        """
        Set cookie policy using long-lived cookie.
        """
        expires = timezone.now() + datetime.timedelta(days=365)
        cookie_policy = {'usage': accepted}
        response.set_cookie(self.cookie_name, json.dumps(cookie_policy), expires=expires, secure=True, httponly=True)