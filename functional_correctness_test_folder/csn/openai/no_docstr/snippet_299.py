
import socket
from typing import Callable, Iterable, Optional, Union


class _AddressListener:
    """
    A simple address listener that forwards incoming messages to a subscriber
    while optionally filtering by service names and resolving hostnames.
    """

    def __init__(
        self,
        subscriber: Union[Callable[[dict], None], object],
        services: str = "",
        nameserver: str = "localhost",
    ):
        """
        Parameters
        ----------
        subscriber
            A callable or an object that will receive processed messages.
            If an object, it must provide a ``handle_msg`` or ``on_address`` method.
        services
            Comma‑separated list of service names to filter on. If empty, all
            services are accepted.
        nameserver
            Hostname of the DNS server to use for hostname resolution. This
            value is passed to ``socket.gethostbyname_ex``; if resolution fails,
            the message is passed unchanged.
        """
        self.subscriber = subscriber
        self.services = (
            [s.strip() for s in services.split(",")
             if s.strip()] if services else None
        )
        self.nameserver = nameserver

    def _resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve a hostname to an IP address using the configured nameserver.
        Returns the first IP address found or None if resolution fails.
        """
        try:
            # ``socket.gethostbyname_ex`` uses the system resolver; we cannot
            # directly specify a nameserver without external libraries, so we
            # simply use the default resolver. The ``nameserver`` attribute is
            # kept for compatibility with potential future extensions.
            _, _, addrs = socket.gethostbyname_ex(hostname)
            return addrs[0] if addrs else None
        except Exception:
            return None

    def _dispatch(self, msg: dict) -> None:
        """
        Dispatch the message to the subscriber. Supports both callables and
        objects with ``handle_msg`` or ``on_address`` methods.
        """
        if callable(self.subscriber):
            self.subscriber(msg)
        else:
            if hasattr(self.subscriber, "handle_msg"):
                self.subscriber.handle_msg(msg)
            elif hasattr(self.subscriber, "on_address"):
                self.subscriber.on_address(msg)
            else:
                raise AttributeError(
                    "Subscriber must be callable or provide a "
                    "'handle_msg' or 'on_address' method."
                )

    def handle_msg(self, msg: dict) -> None:
        """
        Process an incoming message.

        The message is expected to be a dictionary that may contain the keys
        ``service`` and ``hostname``. If a ``service`` filter is configured,
        the message is ignored unless its ``service`` value matches one of the
        configured services. If a ``hostname`` key is present, the listener
        attempts to resolve it to an IP address and adds an ``ip`` key to the
        message.

        Parameters
        ----------
        msg
            The incoming message dictionary.
        """
        if not isinstance(msg, dict):
            raise TypeError("Message must be a dictionary")

        # Service filtering
        if self.services is not None:
            service = msg.get("service")
            if service not in self.services:
                return  # ignore message

        # Hostname resolution
        hostname = msg.get("hostname")
        if isinstance(hostname, str):
            ip = self._resolve_hostname(hostname)
            if ip:
                msg["ip"] = ip

        # Dispatch to subscriber
        self._dispatch(msg)
