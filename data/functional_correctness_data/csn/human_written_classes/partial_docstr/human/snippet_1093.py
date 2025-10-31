import configparser
import os
from django.core.exceptions import ImproperlyConfigured

class Config:
    config_file = None
    config = None
    is_production = None

    def __init__(self, config_files):
        """
        Creates a new config object.

        Parameters:
        config_files: Dictionary with file_name: is_production setting
        """
        for config_file, is_production in config_files:
            if os.path.isfile(config_file):
                self.config_file = config_file
                self.is_production = is_production
                self.config = configparser.SafeConfigParser()
                self.config.read([self.config_file], encoding='utf-8')
                return
        raise IOError('No configuration file found.')

    def has_option(self, name, category):
        return self.config.has_option(name, category)

    def get_bool(self, name, category, default):
        if not self.has_option(name, category):
            return default
        text = self.get(name, category)
        return text.lower() in ['true', 't', 'yes', 'active', 'enabled']

    def get(self, name, category, mandatory=False, expect_leading_slash=None, expect_trailing_slash=None):
        try:
            text = self.config.get(name, category)
        except configparser.NoOptionError:
            if not mandatory:
                return ''
            else:
                raise ImproperlyConfigured(name + ' not set in the config file.')
        except configparser.NoSectionError:
            if not mandatory:
                return ''
            else:
                raise ImproperlyConfigured(category + ' section not set in the config file.')
        logtext = "Setting '[%s] %s' in %s has the value '%s'" % (category, name, self.config_file, text)
        if mandatory and text == NOT_CONFIGURED_VALUE:
            raise ImproperlyConfigured(logtext + ', but must be set.')
        if len(text) == 0:
            if expect_leading_slash or expect_trailing_slash:
                raise ImproperlyConfigured(logtext + ', but should not be empty.')
        else:
            if not text[0] == '/' and expect_leading_slash is True:
                raise ImproperlyConfigured(logtext + ', but should have a leading slash.')
            if not text[-1] == '/' and expect_trailing_slash is True:
                raise ImproperlyConfigured(logtext + ', but should have a trailing slash.')
            if text[0] == '/' and expect_leading_slash is False:
                raise ImproperlyConfigured(logtext + ", but shouldn't have a leading slash.")
            if text[-1] == '/' and expect_trailing_slash is False:
                raise ImproperlyConfigured(logtext + ", but shouldn't have a trailing slash.")
        return text