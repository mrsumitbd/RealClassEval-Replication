import yaml
from reana_commons.errors import REANAConfigDoesNotExist
import os

class REANAConfig:
    """REANA global configuration class."""
    path = '/var/reana/config'
    config_mapping = {'ui': 'ui-config.yaml'}

    @classmethod
    def _read_file(cls, filename):
        with open(os.path.join(cls.path, filename)) as yaml_file:
            data = yaml.load(yaml_file, Loader=yaml.FullLoader)
            return data

    @classmethod
    def load(cls, kind):
        """REANA-UI configuration."""
        if kind not in cls.config_mapping:
            raise REANAConfigDoesNotExist('{} configuration does not exist'.format(kind))
        return cls._read_file(cls.config_mapping[kind])