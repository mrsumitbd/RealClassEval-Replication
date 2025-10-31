from abc import ABC, abstractmethod


class Subscriber(ABC):
    '''Abstract Subscriber class.'''

    @abstractmethod
    def update_property(self, property_):
        '''
        Send an update about a Property.
        :param property_: Property
        '''
        raise NotImplementedError

    @abstractmethod
    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        raise NotImplementedError

    @abstractmethod
    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        raise NotImplementedError
