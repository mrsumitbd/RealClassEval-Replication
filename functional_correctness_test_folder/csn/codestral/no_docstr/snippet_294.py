
class ListenerContainer:

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services
        self.listeners = []

    def __setstate__(self, state):
        self.__dict__ = state
        self.listeners = []

    def restart_listener(self, topics):
        self.stop()
        self.topics = topics
        for topic in self.topics:
            listener = Listener(topic, self.addresses,
                                self.nameserver, self.services)
            self.listeners.append(listener)

    def stop(self):
        for listener in self.listeners:
            listener.stop()
        self.listeners = []


class Listener:

    def __init__(self, topic, addresses, nameserver, services):
        self.topic = topic
        self.addresses = addresses
        self.nameserver = nameserver
        self.services = services
        self.running = True

    def stop(self):
        self.running = False
