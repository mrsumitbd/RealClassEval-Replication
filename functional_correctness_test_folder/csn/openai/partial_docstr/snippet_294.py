
import threading
import time
import pickle


class ListenerContainer:
    '''Container for a listener instance.'''

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        '''Initialize the class.'''
        self.topics = topics or []
        self.addresses = addresses or []
        self.nameserver = nameserver
        self.services = services
        self._stop_event = threading.Event()
        self._thread = None
        self._start_listener()

    def _start_listener(self):
        '''Internal helper to start the listener thread.'''
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._listener_loop, daemon=True)
        self._thread.start()

    def _listener_loop(self):
        '''Simulated listener loop.'''
        while not self._stop_event.is_set():
            # Simulate listening activity
            print(f"[Listener] Listening on topics: {self.topics} "
                  f"addresses: {self.addresses} nameserver: {self.nameserver} "
                  f"services: {self.services}")
            time.sleep(1)

    def __setstate__(self, state):
        '''Restore state after unpickling.'''
        self.__dict__.update(state)
        # Recreate transient attributes
        if not hasattr(self, '_stop_event') or self._stop_event is None:
            self._stop_event = threading.Event()
        if not hasattr(self, '_thread') or self._thread is None:
            self._thread = None
        # Restart listener if it was running before pickling
        if state.get('_running', False):
            self._start_listener()

    def restart_listener(self, topics):
        '''Restart listener after configuration update.'''
        self.stop()
        self.topics = topics or []
        self._start_listener()

    def stop(self):
        '''Stop the listener thread.'''
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join(timeout=5)
            self._thread = None

    def __del__(self):
        '''Ensure cleanup on deletion.'''
        self.stop()
