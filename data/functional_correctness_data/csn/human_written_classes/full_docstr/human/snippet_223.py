import logging
import json

class LoggerBackend:
    """
    Event tracker backend that uses a python logger.

    Events are logged to the INFO level as JSON strings.
    """

    def __init__(self, **kwargs):
        """
        Event tracker backend that uses a python logger.

        `name` is an identifier for the logger, which should have
            been configured using the default python mechanisms.
        """
        name = kwargs.get('name', None)
        self.max_event_size = kwargs.get('max_event_size', MAX_EVENT_SIZE)
        self.event_logger = logging.getLogger(name)
        level = kwargs.get('level', 'info')
        self.log = getattr(self.event_logger, level.lower())

    def send(self, event):
        """Send the event to the standard python logger"""
        event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        if self.max_event_size is None or len(event_str) <= self.max_event_size:
            self.log(event_str)