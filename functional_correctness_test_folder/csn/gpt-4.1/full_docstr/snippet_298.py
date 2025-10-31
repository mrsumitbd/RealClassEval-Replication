
# Assuming _MAGICK is a sentinel value, define it here
_MAGICK = object()


class DummySubscriber:
    """A dummy subscriber to simulate message receiving."""

    def __init__(self, services, topics, addr_listener, addresses, timeout, translate, nameserver, message_filter):
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter
        self.active = False

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def recv(self):
        # Dummy generator for demonstration
        for i in range(3):
            yield f"Message {i+1} from {self.services} on {self.topics}"


def create_subscriber_from_dict_config(services, topics, addr_listener, addresses, timeout, translate, nameserver, message_filter):
    # For demonstration, always return DummySubscriber
    return DummySubscriber(services, topics, addr_listener, addresses, timeout, translate, nameserver, message_filter)


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
        self._subscriber = create_subscriber_from_dict_config(
            self.services,
            self.topics,
            self.addr_listener,
            self.addresses,
            self.timeout,
            self.translate,
            self.nameserver,
            self.message_filter
        )
        self._subscriber.start()
        return self._subscriber

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Stop the subscriber when used as a context manager.'''
        if self._subscriber:
            self._subscriber.stop()
        self._subscriber = None
