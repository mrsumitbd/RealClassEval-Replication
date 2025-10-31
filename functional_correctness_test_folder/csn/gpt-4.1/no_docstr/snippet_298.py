
class Subscribe:
    _MAGICK = object()  # placeholder for the default value

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        self.services = services
        if topics is Subscribe._MAGICK:
            self.topics = []
        else:
            self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses if addresses is not None else []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self.active = False

    def __enter__(self):
        self.active = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.active = False
