from django.conf import settings as django_settings
import os

class XRaySettings:
    """
    A object of Django settings to easily modify certain fields.
    The precedence for configurations at different places is as follows:
    environment variables > user settings in settings.py > default settings
    """

    def __init__(self, user_settings=None):
        self.defaults = DEFAULTS
        if user_settings:
            self._user_settings = user_settings

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(django_settings, XRAY_NAMESPACE, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid setting: %s' % attr)
        if self.user_settings.get(attr, None) is not None:
            if attr in SUPPORTED_ENV_VARS:
                return os.getenv(attr, self.user_settings[attr])
            else:
                return self.user_settings[attr]
        elif attr in SUPPORTED_ENV_VARS:
            return os.getenv(attr, self.defaults[attr])
        else:
            return self.defaults[attr]