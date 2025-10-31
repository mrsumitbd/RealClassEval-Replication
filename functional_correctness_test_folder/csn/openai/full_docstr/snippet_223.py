
import json
import logging


class LoggerBackend:
    '''
    Event tracker backend that uses a python logger.
    Events are logged to the INFO level as JSON strings.
    '''

    def __init__(self, **kwargs):
        '''
        Event tracker backend that uses a python logger.
        `name` is an identifier for the logger, which should have
            been configured using the default python mechanisms.
        '''
        name = kwargs.get('name')
        if not name:
            raise ValueError(
                "LoggerBackend requires a 'name' keyword argument")
        self.logger = logging.getLogger(name)

    def send(self, event):
        '''Send the event to the standard python logger'''
        try:
            message = json.dumps(event)
        except (TypeError, ValueError):
            message = str(event)
        self.logger.info(message)
