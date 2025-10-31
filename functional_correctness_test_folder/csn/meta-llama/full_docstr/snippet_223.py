
import logging
import json


class LoggerBackend:
    '''
    Event tracker backend that uses a python logger.
    Events are logged to the INFO level as JSON strings.
    '''

    def __init__(self, name, **kwargs):
        '''
        Event tracker backend that uses a python logger.
        `name` is an identifier for the logger, which should have
            been configured using the default python mechanisms.
        '''
        self.logger = logging.getLogger(name)

    def send(self, event):
        '''Send the event to the standard python logger'''
        self.logger.info(json.dumps(event))
