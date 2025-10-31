
import posttroll.subscriber

_MAGICK = "all"


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
        self.subscriber = posttroll.subscriber.create_subscriber_from_dict_config({
            'services': services,
            'topics': topics,
            'addr_listener': addr_listener,
            'addresses': addresses,
            'timeout': timeout,
            'translate': translate,
            'nameserver': nameserver,
            'message_filter': message_filter
        })

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self.subscriber.start()
        return self.subscriber

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Stop the subscriber when used as a context manager.'''
        self.subscriber.stop()
