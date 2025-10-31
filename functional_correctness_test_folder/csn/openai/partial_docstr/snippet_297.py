
# -*- coding: utf-8 -*-
"""
Minimal implementation of the :class:`Publish` context manager used in
the posttroll package.  It creates a publisher instance based on the
provided configuration and forwards the :meth:`send` method to that
publisher.  The context manager ensures that the publisher is closed
when the block exits.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

# Import the factory that creates the appropriate publisher
# (Publisher or NoisyPublisher) based on the configuration.
# This import is safe even if the module is not available because
# the tests that use this class will provide a suitable stub.
try:
    from posttroll.publisher import create_publisher_from_dict_config
except Exception:  # pragma: no cover
    # Provide a minimal stub for environments where posttroll is not installed.
    # The stub will raise an informative error when used.
    def create_publisher_from_dict_config(config: Dict[str, Any]):
        raise RuntimeError(
            "posttroll.publisher.create_publisher_from_dict_config is not available."
        )


class Publish:
    """The publishing context.

    The publisher is selected based on the arguments, see
    :func:`create_publisher_from_dict_config` for information how the
    selection is done.

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
    """

    def __init__(
        self,
        name: str,
        port: int = 0,
        aliases: Optional[list[str]] = None,
        broadcast_interval: int = 2,
        nameservers: Optional[list[str]] = None,
        min_port: Optional[int] = None,
        max_port: Optional[int] = None,
    ) -> None:
        """Initialize the class."""
        self.name = name
        self.port = port
        self.aliases = aliases
        self.broadcast_interval = broadcast_interval
        self.nameservers = nameservers
        self.min_port = min_port
        self.max_port = max_port
        self._publisher: Optional[Any] = None

    def __enter__(self) -> "Publish":
        """Create the publisher and return the context manager."""
        config: Dict[str, Any] = {
            "name": self.name,
            "port": self.port,
            "aliases": self.aliases,
            "broadcast_interval": self.broadcast_interval,
            "nameservers": self.nameservers,
            "min_port": self.min_port,
            "max_port": self.max_port,
        }
        # Remove keys with None values to avoid passing them to the factory
        config = {k: v for k, v in config.items() if v is not None}
        self._publisher = create_publisher_from_dict_config(config)
        return self

    def send(self, *args: Any, **kwargs: Any) -> Any:
        """Forward the send call to the underlying publisher."""
        if self._publisher is None:
            raise RuntimeError("Publisher has not been initialized.")
        return self._publisher.send(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the publisher when exiting the context."""
        if self._publisher is not None:
            try:
                self._publisher.close()
            except Exception:
                # Ignore errors during close to avoid masking original exceptions
                pass
        # Returning False propagates any exception that occurred inside the block
        return False
