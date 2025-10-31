import os
import yaml

class Config:
    """
    A collection of configuration data used throughout this script
    """

    def __init__(self, reserved_keyword_config_file, override_file, report_path, report_file, system):
        reserved_keyword_config = self.read_config_file(reserved_keyword_config_file)
        if system:
            try:
                self.reserved_keyword_config = {system: reserved_keyword_config[system]}
            except KeyError:
                raise ConfigurationException(f'Parameter {system} missing from config file {reserved_keyword_config_file}')
        else:
            self.reserved_keyword_config = reserved_keyword_config
        self.override_file = override_file
        if override_file:
            self.overrides = self.read_config_file(override_file)
        else:
            self.overrides = {}
        self.validate_override_config()
        self.report_path = report_path
        self.report_file = os.path.join(report_path, report_file)

    @staticmethod
    def read_config_file(config_file_path):
        log.info('Loading config file: {}'.format(config_file_path))
        try:
            config_dict = yaml.safe_load(config_file_path)
            for key in list(config_dict.keys()):
                if not config_dict[key]:
                    config_dict[key] = []
        except (yaml.parser.ParserError, FileNotFoundError):
            raise ConfigurationException(f'Unable to load config file: {config_file_path}')
        if not config_dict:
            raise ConfigurationException(f'Config file is empty: {config_file_path}')
        return config_dict

    def validate_override_config(self):
        invalid_chars = [' ', ',', '-']

        def check(s):
            return any([c in invalid_chars for c in s])
        for system, override_list in list(self.overrides.items()):
            for pattern in override_list:
                try:
                    model_name, field_name = pattern.split('.')
                    if not model_name[0].isupper():
                        log.error('Model names must be camel case')
                        raise ValueError()
                    if check(field_name) or check(model_name):
                        log.error('Invalid character found')
                        raise ValueError()
                except ValueError:
                    raise ConfigurationException(f'Invalid value in override file: {pattern}')