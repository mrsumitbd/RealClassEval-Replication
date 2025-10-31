import logging

class LoggerStreamWriter:
    """
    'Stream' that allows to write to a logger.

    Parameters
    ----------
    logger_name: str
        Name of the logger
    level: int
        Logging level
    """

    def __init__(self, logger_name, level):
        self._logger = logging.getLogger(logger_name)
        self._level = level

    def write(self, message):
        """
        Write to stream.

        Parameters
        ----------
        message: str
        """
        message = message.strip()
        if message != '':
            self._logger.log(self._level, message)