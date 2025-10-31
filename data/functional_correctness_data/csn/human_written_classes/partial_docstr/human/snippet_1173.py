class APISettings:
    """
    A settings object, that allows API settings to accessed as properties
    """

    def __init__(self, app_settings=None, defaults=None, import_strings=None):
        if app_settings:
            self._app_settings = app_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def app_settings(self):
        if not hasattr(self, '_app_settings'):
            self._app_settings = {}
        return self._app_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid API setting: `{}`'.format(attr))
        try:
            val = self.app_settings[attr]
        except KeyError:
            val = self.defaults[attr]
        if attr in self.import_strings:
            val = perform_import(val, attr)
        setattr(self, attr, val)
        return val