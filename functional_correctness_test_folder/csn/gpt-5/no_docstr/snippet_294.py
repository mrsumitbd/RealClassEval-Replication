class ListenerContainer:
    import threading
    import logging
    import time

    class _Listener:
        def __init__(self, topic, address=None, logger=None):
            self.topic = topic
            self.address = address
            self._stop_event = ListenerContainer.threading.Event()
            self._thread = None
            self._logger = logger or ListenerContainer.logging.getLogger(
                __name__)

        def start(self):
            if self._thread and self._thread.is_alive():
                return
            self._thread = ListenerContainer.threading.Thread(
                target=self._run, name=f"Listener-{self.topic}", daemon=True)
            self._thread.start()

        def _run(self):
            # Dummy loop to simulate a listener lifecycle
            self._logger.debug(
                "Listener started for topic=%s address=%s", self.topic, self.address)
            while not self._stop_event.is_set():
                # In a real implementation this would block on I/O
                self._stop_event.wait(0.5)
            self._logger.debug("Listener stopping for topic=%s", self.topic)

        def stop(self, timeout=2.0):
            self._stop_event.set()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout)

        def is_alive(self):
            return self._thread.is_alive() if self._thread else False

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        self._log = self.logging.getLogger(self.__class__.__name__)
        self._lock = self.threading.RLock()

        self.nameserver = nameserver
        self.services = services

        self.topics = self._normalize_topics(topics)
        self.addresses = self._normalize_addresses(addresses, self.topics)

        self._listeners = {}
        self._running = False

        if self.topics:
            self._start_listeners(self.topics)

    def __setstate__(self, state):
        with self._lock:
            self.nameserver = state.get('nameserver', 'localhost')
            self.services = state.get('services', '')
            self.topics = self._normalize_topics(state.get('topics'))
            self.addresses = self._normalize_addresses(
                state.get('addresses'), self.topics)
            self._listeners = {}
            self._running = False
            if self.topics:
                self._start_listeners(self.topics)

    def restart_listener(self, topics):
        new_topics = self._normalize_topics(topics)
        with self._lock:
            to_stop = set(self._listeners.keys()) - new_topics
            to_start = new_topics - set(self._listeners.keys())

            for t in to_stop:
                lst = self._listeners.pop(t, None)
                if lst:
                    try:
                        lst.stop()
                    except Exception:
                        self._log.exception(
                            "Error stopping listener for topic=%s", t)

            # Update topics and addresses mapping
            self.topics = new_topics
            self.addresses = self._normalize_addresses(
                self.addresses, self.topics)

            for t in to_start:
                addr = self._resolve_address_for_topic(t)
                listener = self._Listener(
                    topic=t, address=addr, logger=self._log)
                self._listeners[t] = listener
                try:
                    listener.start()
                except Exception:
                    self._log.exception(
                        "Error starting listener for topic=%s", t)

            self._running = bool(self._listeners)

    def stop(self):
        with self._lock:
            for t, lst in list(self._listeners.items()):
                try:
                    lst.stop()
                except Exception:
                    self._log.exception(
                        "Error stopping listener for topic=%s", t)
            self._listeners.clear()
            self._running = False

    # Internal helpers
    def _start_listeners(self, topics):
        with self._lock:
            for t in topics:
                if t in self._listeners:
                    continue
                addr = self._resolve_address_for_topic(t)
                listener = self._Listener(
                    topic=t, address=addr, logger=self._log)
                self._listeners[t] = listener
                listener.start()
            self._running = bool(self._listeners)

    def _normalize_topics(self, topics):
        if topics is None:
            return set()
        if isinstance(topics, (set, list, tuple)):
            return {str(t) for t in topics if t is not None}
        return {str(topics)}

    def _normalize_addresses(self, addresses, topics):
        if not topics:
            return {}
        topics_list = list(topics)
        # If addresses is a mapping, filter to topics
        if isinstance(addresses, dict):
            return {str(k): addresses[k] for k in map(str, topics_list) if k in addresses}
        # If addresses is a list/tuple aligned with topics
        if isinstance(addresses, (list, tuple)):
            result = {}
            for i, t in enumerate(topics_list):
                result[str(t)] = addresses[i] if i < len(addresses) else None
            return result
        # Single address for all topics
        if addresses is None:
            default = None
        else:
            default = addresses
        return {str(t): default for t in topics_list}

    def _resolve_address_for_topic(self, topic):
        key = str(topic)
        if key in self.addresses:
            return self.addresses[key]
        # Fallback default
        return None
