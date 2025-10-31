
import threading
import time

# Sentinel value used to indicate that no specific topics were supplied
_MAGICK = object()


class Subscribe:
    """
    A simple context‑manager based subscription helper.

    Parameters
    ----------
    services : str, optional
        Comma separated list of services to subscribe to.
    topics : str or list, optional
        Topics to filter on. If omitted, all topics are accepted.
    addr_listener : bool, optional
        If True, a background thread will be started that pretends to
        listen for address updates. This is a no‑op placeholder.
    addresses : list, optional
        List of addresses to connect to. If None, a default address is used.
    timeout : int, optional
        Timeout in seconds for the subscription to be considered alive.
    translate : bool, optional
        If True, messages will be passed through a dummy translation step.
    nameserver : str, optional
        Name of the nameserver to use for service discovery.
    message_filter : callable, optional
        A callable that receives a message and returns True if the message
        should be processed.
    """

    def __init__(
        self,
        services="",
        topics=_MAGICK,
        addr_listener=False,
        addresses=None,
        timeout=10,
        translate=False,
        nameserver="localhost",
        message_filter=None,
    ):
        # Store raw parameters
        self.services = services
        self._raw_topics = topics
        self.addr_listener = addr_listener
        self.addresses = addresses or ["tcp://localhost:5555"]
        self.timeout = timeout
        self.translate = translate
        self.nameserver = nameserver
        self.message_filter = message_filter

        # Normalise services and topics
        self.service_list = [s.strip()
                             for s in services.split(",") if s.strip()]
        if topics is _MAGICK:
            self.topics = ["*"]
        elif isinstance(topics, str):
            self.topics = [t.strip() for t in topics.split(",") if t.strip()]
        else:
            self.topics = list(topics)

        # Internal state
        self._subscribed = False
        self._listener_thread = None
        self._stop_event = threading.Event()

    def __enter__(self):
        """
        Enter the runtime context related to this object.
        Sets up the subscription and starts the address listener if requested.
        """
        # Simulate subscription setup
        self._subscribed = True
        if self.addr_listener:
            self._start_listener()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and clean up resources.
        """
        # Stop listener thread if running
        if self.addr_listener:
            self._stop_listener()
        # Simulate unsubscription
        self._subscribed = False
        # Returning False propagates any exception that occurred
        return False

    # ------------------------------------------------------------------
    # Helper methods for the dummy address listener
    # ------------------------------------------------------------------
    def _start_listener(self):
        """Start a background thread that pretends to listen for address updates."""
        if self._listener_thread and self._listener_thread.is_alive():
            return
        self._stop_event.clear()
        self._listener_thread = threading.Thread(
            target=self._listener_loop, daemon=True
        )
        self._listener_thread.start()

    def _stop_listener(self):
        """Signal the listener thread to stop and wait for it."""
        if self._listener_thread and self._listener_thread.is_alive():
            self._stop_event.set()
            self._listener_thread.join(timeout=self.timeout)
            self._listener_thread = None

    def _listener_loop(self):
        """Dummy loop that periodically prints a message."""
        while not self._stop_event.is_set():
            # In a real implementation this would handle address updates.
            time.sleep(1)

    # ------------------------------------------------------------------
    # Public API for sending/receiving messages (dummy)
    # ------------------------------------------------------------------
    def receive(self):
        """
        Dummy method that simulates receiving a message.
        Returns a dictionary with service, topic, and payload.
        """
        if not self._subscribed:
            raise RuntimeError("Not subscribed")
        # Simulate a message
        msg = {"service": self.service_list[0] if self.service_list else None,
               "topic": self.topics[0] if self.topics else None,
               "payload": "dummy payload"}
        # Apply translation if requested
        if self.translate:
            msg = self._translate(msg)
        # Apply message filter if provided
        if self.message_filter and not self.message_filter(msg):
            return None
        return msg

    def _translate(self, msg):
        """Dummy translation step."""
        msg["payload"] = f"translated:{msg['payload']}"
        return msg
