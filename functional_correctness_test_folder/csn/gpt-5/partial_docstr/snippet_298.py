import time

# Provide a local sentinel if not defined elsewhere
try:
    _MAGICK
except NameError:
    _MAGICK = object()


class Subscribe:

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        '''Initialize the class.'''
        self.services = self._normalize_to_tuple(services)
        if topics is _MAGICK:
            self.topics = self.services
        else:
            self.topics = self._normalize_to_tuple(topics)
        self.addr_listener = bool(addr_listener)
        self.addresses = tuple(addresses) if addresses is not None else tuple()
        self.timeout = float(timeout) if timeout is not None else 10.0
        self.translate = bool(translate)
        self.nameserver = str(
            nameserver) if nameserver is not None else 'localhost'
        if message_filter is not None and not callable(message_filter):
            raise TypeError("message_filter must be callable or None")
        self.message_filter = message_filter

        self.active = False
        self.started_at = None

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self.active = True
        self.started_at = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
        self.started_at = None
        return False

    @staticmethod
    def _normalize_to_tuple(value):
        if value is None:
            return tuple()
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return tuple()
            # Split on commas or whitespace
            parts = [p for chunk in stripped.split(
                ',') for p in chunk.split() if p]
            return tuple(parts)
        try:
            return tuple(value)
        except TypeError:
            return (value,)
