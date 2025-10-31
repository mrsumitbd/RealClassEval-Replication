
import threading
import time
import pickle


class ListenerContainer:
    """
    A simple listener container that simulates listening to topics.
    """

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        """
        Initialize the listener container.

        :param topics: Iterable of topics to listen to.
        :param addresses: Iterable of addresses (unused in this simple implementation).
        :param nameserver: Name server address (unused in this simple implementation).
        :param services: Services string (unused in this simple implementation).
        """
        self.topics = list(topics) if topics is not None else []
        self.addresses = list(addresses) if addresses is not None else []
        self.nameserver = nameserver
        self.services = services

        # Thread control
        self._stop_event = threading.Event()
        self._thread = None
        self._start_listener()

    def __setstate__(self, state):
        """
        Restore the state of the object after unpickling.
        """
        self.__dict__.update(state)
        # Ensure the stop event and thread are reset
        if not hasattr(self, '_stop_event') or self._stop_event is None:
            self._stop_event = threading.Event()
        if not hasattr(self, '_thread') or self._thread is None:
            self._thread = None
        # Restart the listener after unpickling
        self._start_listener()

    def _listener_loop(self):
        """
        The main loop that simulates listening to topics.
        """
        while not self._stop_event.is_set():
            if self.topics:
                # Simulate processing each topic
                for topic in self.topics:
                    if self._stop_event.is_set():
                        break
                    # In a real implementation, this would be where messages are received.
                    print(f"[Listener] Processing topic: {topic}")
                    time.sleep(0.1)
            else:
                # No topics to listen to; just wait a bit
                time.sleep(0.5)

    def _start_listener(self):
        """
        Start the listener thread.
        """
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._listener_loop, daemon=True)
        self._thread.start()

    def restart_listener(self, topics):
        """
        Restart the listener with a new set of topics.

        :param topics: Iterable of new topics to listen to.
        """
        # Stop current listener
        self.stop()
        # Update topics
        self.topics = list(topics) if topics is not None else []
        # Restart listener
        self._start_listener()

    def stop(self):
        """
        Stop the listener thread.
        """
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=1.0)
            self._thread = None

    def __del__(self):
        """
        Ensure the listener thread is stopped when the object is garbage collected.
        """
        self.stop()


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     lc = ListenerContainer(topics=['topic1', 'topic2'])
#     time.sleep(1)
#     lc.restart_listener(['topic3'])
#     time.sleep(1)
#     lc.stop()
