import logging
from zsl.interface.cli import cli

class ZslCli:

    def __init__(self):
        logging.getLogger(__name__).debug('Creating ZSL CLI.')
        self._cli = cli

    @property
    def cli(self):
        return self._cli

    def __call__(self, *args, **kwargs):
        cli(**kwargs)