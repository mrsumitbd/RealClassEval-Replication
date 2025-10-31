
class ListenerContainer:

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services
        self.running = True
        self.listeners = {}
        self._init_listeners()

    def _init_listeners(self):
        for topic in self.topics:
            self.listeners[topic] = f"Listener for {topic}"

    def __setstate__(self, state):
        self.__dict__.update(state)
        if 'listeners' not in self.__dict__:
            self.listeners = {}
        self._init_listeners()

    def restart_listener(self, topics):
        for topic in topics:
            self.listeners[topic] = f"Listener for {topic}"

    def stop(self):
        self.running = False
        self.listeners.clear()
