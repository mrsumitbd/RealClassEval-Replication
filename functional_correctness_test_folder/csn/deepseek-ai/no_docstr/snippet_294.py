
class ListenerContainer:

    def __init__(self, topics=None, addresses=None, nameserver='localhost', services=''):
        self.topics = topics if topics is not None else []
        self.addresses = addresses if addresses is not None else []
        self.nameserver = nameserver
        self.services = services

    def __setstate__(self, state):
        self.__dict__.update(state)

    def restart_listener(self, topics):
        self.topics = topics

    def stop(self):
        pass
