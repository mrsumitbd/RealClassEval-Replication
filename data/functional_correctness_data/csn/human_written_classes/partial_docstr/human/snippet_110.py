from django.conf import settings

class GrapheneSettings:
    """
    A settings object, that allows API settings to be accessed as properties.
    For example:
        from graphene_django.settings import settings
        print(settings.SCHEMA)
    Any setting with string import paths will be automatically resolved
    and return the class, rather than the string literal.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRAPHENE', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid Graphene setting: '%s'" % attr)
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]
        if attr in self.import_strings:
            val = perform_import(val, attr)
        setattr(self, attr, val)
        return val