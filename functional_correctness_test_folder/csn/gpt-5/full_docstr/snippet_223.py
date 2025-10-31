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
        name = kwargs.get('name')
        logger = kwargs.get('logger')
        self.level = kwargs.get('level', logging.INFO)
        self.ensure_ascii = kwargs.get('ensure_ascii', False)
        self.json_encoder = kwargs.get('json_encoder', None)

        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(
                name) if name else logging.getLogger()

    def _json_default(self, obj):
        for attr in ('to_dict', 'dict', 'model_dump'):
            fn = getattr(obj, attr, None)
            if callable(fn):
                try:
                    return fn()
                except Exception:
                    pass
        try:
            return vars(obj)
        except Exception:
            return str(obj)

    def send(self, event):
        '''Send the event to the standard python logger'''
        try:
            payload = json.dumps(
                event,
                ensure_ascii=self.ensure_ascii,
                cls=self.json_encoder,
                default=self._json_default,
                separators=(',', ':')
            )
        except Exception:
            payload = json.dumps(
                {'error': 'failed to serialize event', 'repr': repr(event)},
                ensure_ascii=self.ensure_ascii,
                separators=(',', ':')
            )
        self.logger.log(self.level, payload)
