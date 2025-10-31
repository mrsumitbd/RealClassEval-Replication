class SettingsMixin:
    _settings = None

    def __init__(self, *args, **kwargs):
        self.custom_settings = kwargs.pop('settings', None)
        super().__init__(*args, **kwargs)

    @property
    def settings(self):
        _settings = self._settings.copy()
        if self.custom_settings is not None:
            assert isinstance(self.custom_settings, dict), '`settings` argument must be a dict type'
            _settings.update(self.custom_settings)
        return _settings

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['settings'] = self.settings
        return context