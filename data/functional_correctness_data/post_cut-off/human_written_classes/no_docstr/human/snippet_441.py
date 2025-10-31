import tempfile
import logging
from pydantic import SecretStr
from pathlib import Path

class _TemporaryKeyFile:

    def __init__(self, private_key: SecretStr):
        self.private_key = private_key
        self._tempfile = None

    def __enter__(self):
        self._tempfile = tempfile.NamedTemporaryFile('w')
        self._tempfile.write(self.private_key.get_secret_value())
        self._tempfile.flush()
        logging.debug(f'Created temp key file {self._tempfile.name}')
        return self

    def __exit__(self, exc, value, tb):
        result = self._tempfile.__exit__(exc, value, tb)
        self.close()
        return result

    def close(self):
        if self._tempfile is None:
            return
        self._tempfile.close()

    def get_path(self):
        if self._tempfile is None:
            raise ValueError('Temporary key file has not been created yet.')
        return Path(self._tempfile.name)