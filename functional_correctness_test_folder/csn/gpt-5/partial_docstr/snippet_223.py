import logging
import json
from typing import Any


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
        logger = kwargs.get('logger')
        if logger is not None:
            self._logger = logger
        else:
            name = kwargs.get('name', 'event_tracker')
            self._logger = logging.getLogger(name)

    def _json_default(self, obj: Any) -> str:
        try:
            return obj.__dict__
        except Exception:
            return str(obj)

    def send(self, event):
        '''Send the event to the standard python logger'''
        try:
            payload = json.dumps(
                event, default=self._json_default, ensure_ascii=False)
        except Exception:
            payload = json.dumps({"event": str(event)}, ensure_ascii=False)
        self._logger.info(payload)
