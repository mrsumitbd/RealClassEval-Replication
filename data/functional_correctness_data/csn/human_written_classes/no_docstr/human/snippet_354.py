import logging
from sigal.settings import Status

class raise_if_debug:

    def __init__(self):
        self.value = None

    def __enter__(self, *args):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logger.info('Failed to process: %r', exc_value)
            if logger.getEffectiveLevel() == logging.DEBUG:
                return False
            else:
                self.value = Status.FAILURE
        else:
            self.value = Status.SUCCESS
        return True