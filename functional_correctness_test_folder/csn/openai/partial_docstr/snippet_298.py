
# Sentinel value used for default topics
_MAGICK = object()


class Subscribe:
    def __init__(self, services='', topics=_MAGICK, addr_listener=False,
                 addresses=None, timeout=10, translate=False,
                 nameserver='localhost', message_filter=None):
        """Initialize the class."""
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses or []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self._active = False

    def __enter__(self):
        """Start the subscriber when used as a context manager."""
        self._active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the subscriber and clean up."""
        self._active = False
        # Returning False propagates any exception that occurred
        return False
