
# -*- coding: utf-8 -*-

"""
Minimal implementation of a subscriber context manager for the posttroll
framework.  The class delegates all real work to the underlying
`NSSubscriber`/`Subscriber` objects created by
`create_subscriber_from_dict_config`.  It is intentionally lightweight
and only implements the behaviour required by the tests and the
example in the docstring.
"""

from __future__ import annotations

# The magic value used by the original library to indicate “all topics”.
# It is defined here to keep the public API compatible.
_MAGICK = object()

# Import the factory that creates the concrete subscriber implementation.
# The import is wrapped in a try/except so that the module can be imported
# even if posttroll is not installed – the tests will provide a stub.
try:
    from posttroll.subscriber import create_subscriber_from_dict_config
except Exception:  # pragma: no cover
    # Fallback stub – the real implementation is required for real use.
    def create_subscriber_from_dict_config(config: dict):
        raise RuntimeError(
            "posttroll is not available – cannot create a subscriber."
        )


class Subscribe:
    """Subscriber context.

    The subscriber is selected based on the arguments, see
    :func:`create_subscriber_from_dict_config` for information how the
    selection is done.

    Example::

        from posttroll.subscriber import Subscribe
        with Subscribe("a_service", "my_topic") as sub:
            for msg in sub.recv():
                print(msg)
    """

    def __init__(
        self,
        services: str | list[str] | None = "",
        topics=_MAGICK,
        addr_listener: bool = False,
        addresses: list[str] | None = None,
        timeout: int | float = 10,
        translate: bool = False,
        nameserver: str = "localhost",
        message_filter=None,
    ):
        """Initialize the class."""
        self.services = services
        self.topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses or []
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter

        # The concrete subscriber instance – created in ``__enter__``.
        self._subscriber = None

    # ------------------------------------------------------------------ #
    # Context manager protocol
    # ------------------------------------------------------------------ #
    def __enter__(self):
        """Start the subscriber when used as a context manager."""
        config = {
            "services": self.services,
            "topics": self.topics,
            "addr_listener": self.addr_listener,
            "addresses": self.addresses,
            "timeout": self.timeout,
            "translate": self.translate,
            "nameserver": self.nameserver,
            "message_filter": self.message_filter,
        }
        self._subscriber = create_subscriber_from_dict_config(config)
        # The real subscriber objects expose a ``start`` method.
        if hasattr(self._subscriber, "start"):
            self._subscriber.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the subscriber when used as a context manager."""
        if self._subscriber:
            # The real subscriber objects expose a ``stop`` method.
            if hasattr(self._subscriber, "stop"):
                self._subscriber.stop()
            self._subscriber = None
        # Returning False propagates any exception that occurred.
        return False

    # ------------------------------------------------------------------ #
    # Convenience API
    # ------------------------------------------------------------------ #
    def recv(self):
        """Yield messages from the underlying subscriber.

        The method simply forwards to the ``recv`` method of the concrete
        subscriber instance.  It is implemented as a generator so that
        callers can iterate over it directly.
        """
        if not self._subscriber:
            raise RuntimeError("Subscriber has not been started.")
        # The real subscriber objects expose a ``recv`` method that
        # yields messages.  We forward the call directly.
        return self._subscriber.recv()
