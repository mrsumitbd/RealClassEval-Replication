import sys
import logging

class LoggingExceptionHook:

    def __init__(self, logger, level=logging.ERROR):
        self._oldexcepthook = sys.excepthook
        self.logger = logger
        self.level = level
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())

    def __del__(self):
        try:
            try:
                sys.excepthook = self._oldexcepthook
            except AttributeError:
                sys.excepthook = sys.__excepthook__
        except AttributeError:
            pass

    def __call__(self, exc_type, exc_value, traceback):
        self.logger.log(self.level, 'An unhandled exception ocurred:', exc_info=(exc_type, exc_value, traceback))
        self._oldexcepthook(exc_type, exc_value, traceback)