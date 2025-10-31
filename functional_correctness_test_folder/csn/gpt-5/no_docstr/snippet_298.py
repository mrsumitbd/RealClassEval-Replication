_MAGICK = object()


class Subscribe:

    def __init__(self, services='', topics=_MAGICK, addr_listener=False, addresses=None, timeout=10, translate=False, nameserver='localhost', message_filter=None):
        self.addr_listener = bool(addr_listener)
        self.timeout = float(timeout) if timeout is not None else None
        self.translate = bool(translate)
        self.nameserver = str(
            nameserver) if nameserver is not None else 'localhost'

        # Normalize services
        if services is None:
            self.services = []
        elif isinstance(services, str):
            parts = [s.strip() for s in services.replace(
                ';', ',').split(',') if s.strip()]
            self.services = parts
        else:
            self.services = list(services)

        # Normalize topics with sentinel default
        if topics is _MAGICK:
            self.topics = []
        elif topics is None:
            self.topics = []
        elif isinstance(topics, str):
            parts = [t.strip() for t in topics.replace(
                ';', ',').split(',') if t.strip()]
            self.topics = parts
        else:
            self.topics = list(topics)

        # Normalize addresses
        if addresses is None:
            self.addresses = []
        elif isinstance(addresses, str):
            parts = [a.strip() for a in addresses.replace(
                ';', ',').split(',') if a.strip()]
            self.addresses = parts
        else:
            self.addresses = list(addresses)

        # Normalize message_filter
        self.message_filter = None
        if message_filter is not None:
            if callable(message_filter):
                self.message_filter = message_filter
            else:
                try:
                    import re
                    pattern = re.compile(str(message_filter))
                    self.message_filter = lambda msg: bool(
                        pattern.search(msg if isinstance(msg, str) else str(msg)))
                except Exception:
                    # Fallback to string containment
                    needle = str(message_filter)
                    self.message_filter = lambda msg: needle in (
                        msg if isinstance(msg, str) else str(msg))

        self._active = False
        self._closed = False

    def __enter__(self):
        self._active = True
        self._closed = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._active = False
        self._closed = True
        return False
