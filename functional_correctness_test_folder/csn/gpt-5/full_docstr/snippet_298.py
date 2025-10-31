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
        self._config = {
            'services': services,
            'topics': topics,
            'addr_listener': addr_listener,
            'addresses': addresses,
            'timeout': timeout,
            'translate': translate,
            'nameserver': nameserver,
            'message_filter': message_filter,
        }
        self._subscriber = None
        self._entered_obj = None

    def __enter__(self):
        '''Start the subscriber when used as a context manager.'''
        self._subscriber = create_subscriber_from_dict_config(self._config)
        # If underlying object supports context management, enter it and return what it returns
        if hasattr(self._subscriber, "__enter__"):
            self._entered_obj = self._subscriber.__enter__()
            return self._entered_obj if self._entered_obj is not None else self._subscriber
        # Otherwise, try to start it and return the subscriber itself
        start = getattr(self._subscriber, "start", None)
        if callable(start):
            start()
        return self._subscriber

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Stop the subscriber when used as a context manager.'''
        if self._subscriber is None:
            return False
        # Delegate to underlying __exit__ if available
        if hasattr(self._subscriber, "__exit__"):
            return bool(self._subscriber.__exit__(exc_type, exc_val, exc_tb))
        # Otherwise, try to gracefully stop/close
        result = False
        for meth_name in ("stop", "close", "shutdown", "terminate"):
            meth = getattr(self._subscriber, meth_name, None)
            if callable(meth):
                try:
                    meth()
                    result = False
                    break
                except Exception:
                    pass
        return result
