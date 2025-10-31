
class Subscribe:

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
        self.subscriber = None

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self.subscriber = SomeSubscriberLibrary.Subscriber(
            services=self.services,
            topics=self.topics,
            addr_listener=self.addr_listener,
            addresses=self.addresses,
            timeout=self.timeout,
            translate=self.translate,
            nameserver=self.nameserver,
            message_filter=self.message_filter
        )
        self.subscriber.start()
        return self.subscriber

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.subscriber:
            self.subscriber.stop()
            self.subscriber = None
