
import logging


class LoggerBackend:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'LoggerBackend')
        self.level = kwargs.get('level', 'INFO')
        self.file = kwargs.get('file')
        self.formatter = kwargs.get(
            'formatter',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(
            getattr(logging, self.level.upper(), logging.INFO))

        # Remove existing handlers to avoid duplicate logs
        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)

        if self.file:
            handler = logging.FileHandler(self.file)
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(logging.Formatter(self.formatter))
        self.logger.addHandler(handler)

    def send(self, event):
        if isinstance(event, Exception):
            self.logger.exception(str(event))
        else:
            self.logger.info(str(event))
