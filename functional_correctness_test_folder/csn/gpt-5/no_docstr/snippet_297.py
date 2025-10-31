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
        self.name = name
        self.port = port
        self.aliases = aliases
        self.broadcast_interval = broadcast_interval
        self.nameservers = nameservers
        self.min_port = min_port
        self.max_port = max_port

        self._publisher = None
        self._publisher_entered = False
        self._exit_callable = None
        self._closed = False
        self._fallback_messages = []

    def _build_config(self):
        cfg = {
            "name": self.name,
            "port": self.port,
            "aliases": self.aliases,
            "broadcast_interval": self.broadcast_interval,
            "nameservers": self.nameservers,
            "min_port": self.min_port,
            "max_port": self.max_port,
        }
        # Remove None values to let defaults apply
        return {k: v for k, v in cfg.items() if v is not None}

    def _create_publisher(self):
        try:
            # Try to import factory from posttroll if available
            from posttroll.publisher import create_publisher_from_dict_config  # type: ignore
        except Exception:
            create_publisher_from_dict_config = None

        if create_publisher_from_dict_config is None:
            # Fallback dummy publisher
            class _FallbackPublisher:
                def __init__(self, outer):
                    self._outer = outer

                def send(self, data):
                    self._outer._fallback_messages.append(data)

                def close(self):
                    pass

            return _FallbackPublisher(self)

        cfg = self._build_config()
        return create_publisher_from_dict_config(cfg)

    def __enter__(self):
        self._publisher = self._create_publisher()

        # If the underlying publisher is a context manager, enter it
        if hasattr(self._publisher, "__enter__") and hasattr(self._publisher, "__exit__"):
            entered = self._publisher.__enter__()
            # Some __enter__ return self; others return a different handle
            # We will use whatever is returned for sending, but still
            # return this Publish wrapper for stable API.
            if entered is not None:
                self._publisher = entered
            self._publisher_entered = True
            self._exit_callable = getattr(self._publisher, "__exit__", None)
        else:
            # Prepare a generic exit/close routine
            def _generic_exit(exc_type, exc_val, exc_tb):
                # Try common termination methods in order
                for method_name in ("close", "stop", "shutdown", "terminate"):
                    m = getattr(self._publisher, method_name, None)
                    if callable(m):
                        try:
                            m()
                            break
                        except Exception:
                            pass
                return False

            self._exit_callable = _generic_exit

        return self

    def send(self, data):
        if self._closed:
            raise RuntimeError("Publisher is closed")
        sender = getattr(self._publisher, "send", None)
        if callable(sender):
            return sender(data)
        # Fallback: store locally if no sender available
        self._fallback_messages.append(data)
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._closed:
            return False
        try:
            if callable(self._exit_callable):
                return bool(self._exit_callable(exc_type, exc_val, exc_tb))
            return False
        finally:
            self._closed = True
