from abc import ABCMeta

class RouterStrategy:
    __metaclass__ = ABCMeta

    def can_route(self, path):
        pass

    def route(self, path):
        pass