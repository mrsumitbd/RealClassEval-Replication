from abc import ABCMeta, abstractmethod

class SkDataController:
    __metaclass__ = ABCMeta

    def __init__(self, parent, settings: dict={}):
        self.parent = parent
        self.settings = settings

    @abstractmethod
    def display(self):
        """
        This method should be overwritten.
        :return:
        """
        pass