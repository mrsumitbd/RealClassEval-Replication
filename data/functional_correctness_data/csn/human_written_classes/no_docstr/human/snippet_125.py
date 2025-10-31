from django.utils.module_loading import import_string
from django.conf import settings as django_settings

class Settings:

    def __init__(self, default_settings, explicit_overriden_settings: dict=None):
        if explicit_overriden_settings is None:
            explicit_overriden_settings = {}
        overriden_settings = getattr(django_settings, DJOSER_SETTINGS_NAMESPACE, {}) or explicit_overriden_settings
        self._load_default_settings()
        self._override_settings(overriden_settings)
        self._init_settings_to_import()

    def _load_default_settings(self):
        for setting_name, setting_value in default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)

    def _override_settings(self, overriden_settings: dict):
        for setting_name, setting_value in overriden_settings.items():
            value = setting_value
            if isinstance(setting_value, dict):
                value = getattr(self, setting_name, {})
                value.update(ObjDict(setting_value))
            setattr(self, setting_name, value)

    def _init_settings_to_import(self):
        for setting_name in SETTINGS_TO_IMPORT:
            value = getattr(self, setting_name)
            if isinstance(value, str):
                setattr(self, setting_name, import_string(value))