class Publish:
    '''The publishing context.
    See :class:`Publisher` and :class:`NoisyPublisher` for more information on the arguments.
    The publisher is selected based on the arguments, see :func:`create_publisher_from_dict_config` for
    information how the selection is done.
    Example on how to use the :class:`Publish` context::
            from posttroll.publisher import Publish
            from posttroll.message import Message
            import time
            try:
                with Publish("my_service", port=9000) as pub:
                    counter = 0
                    while True:
                        counter += 1
                        message = Message("/counter", "info", str(counter))
                        print("publishing", message)
                        pub.send(message.encode())
                        time.sleep(3)
            except KeyboardInterrupt:
                print("terminating publisher...")
    '''

    def __init__(self, name, port=0, aliases=None, broadcast_interval=2, nameservers=None, min_port=None, max_port=None):
        '''Initialize the class.'''
        self._name = name
        self._port = port
        self._aliases = aliases
        self._broadcast_interval = broadcast_interval
        self._nameservers = nameservers
        self._min_port = min_port
        self._max_port = max_port
        self._publisher = None
        self._entered = False

    def __enter__(self):
        try:
            from posttroll.publisher import create_publisher_from_dict_config
        except Exception as e:
            raise RuntimeError(
                "posttroll.publisher.create_publisher_from_dict_config is not available") from e

        config = {
            "name": self._name,
            "port": self._port,
            "aliases": self._aliases,
            "broadcast_interval": self._broadcast_interval,
            "nameservers": self._nameservers,
            "min_port": self._min_port,
            "max_port": self._max_port,
        }
        self._publisher = create_publisher_from_dict_config(config)

        # If the underlying publisher is a context manager, delegate to it
        if hasattr(self._publisher, "__enter__") and hasattr(self._publisher, "__exit__"):
            self._entered = True
            return self._publisher.__enter__()

        # Otherwise, start it if possible and return the publisher itself
        start = getattr(self._publisher, "start", None)
        if callable(start):
            start()
        self._entered = True
        return self._publisher

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._entered:
            return False

        if self._publisher is None:
            return False

        # Delegate to underlying context manager if available
        if hasattr(self._publisher, "__exit__"):
            return self._publisher.__exit__(exc_type, exc_val, exc_tb)

        # Attempt graceful shutdown methods
        for meth_name in ("stop", "close", "shutdown", "terminate"):
            meth = getattr(self._publisher, meth_name, None)
            if callable(meth):
                try:
                    meth()
                except Exception:
                    pass
                break

        self._publisher = None
        self._entered = False
        return False
