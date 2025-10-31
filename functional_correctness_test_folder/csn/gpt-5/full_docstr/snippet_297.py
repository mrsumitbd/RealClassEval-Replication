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
        self._aliases = list(aliases) if aliases is not None else None
        self._broadcast_interval = broadcast_interval
        self._nameservers = list(
            nameservers) if nameservers is not None else None
        self._min_port = min_port
        self._max_port = max_port

        self._publisher = None
        self._entered_publisher = None  # Result of publisher.__enter__ if it exists

    def _create_publisher(self):
        try:
            # Prefer absolute import path as hinted by the docstring
            from posttroll.publisher import create_publisher_from_dict_config
        except Exception:
            # Fallback to relative/local import if package layout differs
            try:
                from .publisher import create_publisher_from_dict_config  # type: ignore
            except Exception as e:
                raise ImportError(
                    "Could not import create_publisher_from_dict_config") from e

        config = {
            "name": self._name,
            "port": self._port,
            "aliases": self._aliases,
            "broadcast_interval": self._broadcast_interval,
            "nameservers": self._nameservers,
            "min_port": self._min_port,
            "max_port": self._max_port,
        }
        return create_publisher_from_dict_config(config)

    def __enter__(self):
        '''Enter the context.'''
        self._publisher = self._create_publisher()

        # If underlying publisher is a context manager, use it
        enter = getattr(self._publisher, "__enter__", None)
        if callable(enter):
            self._entered_publisher = enter()
            return self._entered_publisher

        # Otherwise, try to "start" or "open" if available
        starter = getattr(self._publisher, "start", None) or getattr(
            self._publisher, "open", None)
        if callable(starter):
            starter()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the context.'''
        # If we used the publisher as a context manager, delegate exit
        if self._entered_publisher is not None:
            exit_method = getattr(self._publisher, "__exit__", None)
            if callable(exit_method):
                return exit_method(exc_type, exc_val, exc_tb)

        # Otherwise, try graceful shutdown methods
        closer = getattr(self._publisher, "stop", None) or getattr(
            self._publisher, "close", None) or getattr(self._publisher, "shutdown", None)
        if callable(closer):
            closer()

        # Cleanup references
        self._entered_publisher = None
        self._publisher = None
        return False

    def send(self, *args, **kwargs):
        if self._publisher is None:
            raise RuntimeError(
                "Publisher is not initialized. Use Publish as a context manager.")
        send_fn = getattr(self._publisher, "send", None)
        if not callable(send_fn):
            raise AttributeError(
                "Underlying publisher does not implement 'send'.")
        return send_fn(*args, **kwargs)

    def __getattr__(self, item):
        # Proxy other attributes/methods to the underlying publisher when available
        if item.startswith("_"):
            raise AttributeError(item)
        pub = object.__getattribute__(self, "_publisher")
        if pub is not None and hasattr(pub, item):
            return getattr(pub, item)
        raise AttributeError(item)
