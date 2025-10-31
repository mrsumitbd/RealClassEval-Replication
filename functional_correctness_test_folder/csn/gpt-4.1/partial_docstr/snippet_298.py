
class Subscribe:
    _MAGICK = object()

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        '''Initialize the class.'''
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses if addresses is not None else []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self.active = False

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
