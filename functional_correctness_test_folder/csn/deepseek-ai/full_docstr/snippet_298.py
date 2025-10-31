
class Subscribe:
    '''Subscriber context.
    See :class:`NSSubscriber` and :class:`Subscriber` for initialization parameters.
    The subscriber is selected based on the arguments, see :func:`create_subscriber_from_dict_config` for
    information how the selection is done.
    Example::
            del tmp
        from posttroll.subscriber import Subscribe
        with Subscribe("a_service", "my_topic",) as sub:
            for msg in sub.recv():
                print(msg)
    '''

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        '''Initialize the class.'''
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self._subscriber = None

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self._subscriber = create_subscriber_from_dict_config({
            'services': self.services,
            'topics': self.topics,
            'addr_listener': self.addr_listener,
            'addresses': self.addresses,
            'timeout': self.timeout,
            'translate': self.translate,
            'nameserver': self.nameserver,
            'message_filter': self.message_filter
        })
        return self._subscriber

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Stop the subscriber when used as a context manager.'''
        if self._subscriber is not None:
            self._subscriber.stop()
