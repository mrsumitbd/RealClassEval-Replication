
import logging
import json


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
        name = kwargs.get('name', __name__)
        self.logger = logging.getLogger(name)

    def send(self, event):
        '''Send the event to the standard python logger'''
        try:
            message = json.dumps(event)
        except (TypeError, ValueError):
            # Fallback: use str representation if not JSON serializable
            message = str(event)
        self.logger.info(message)
