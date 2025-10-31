from django.conf import settings

class HealthCheckSettingsMixin:
    """Mixin that makes settings.HEALTH_CHECK available as property, and supplies empty dict instead if the setting
    is not defined"""

    @property
    def settings(self):
        return getattr(settings, 'HEALTH_CHECK', {})

    @property
    def requests_timeout(self):
        return self.settings.get('REQUESTS_TIMEOUT', 5)