
from abc import ABC, abstractmethod


class Property:
    pass  # Assuming Property class is defined elsewhere


class Action:
    pass  # Assuming Action class is defined elsewhere


class Event:
    pass  # Assuming Event class is defined elsewhere


class Subscriber(ABC):
    '''Abstract Subscriber class.'''

    @abstractmethod
    def update_property(self, property_: Property):
        '''
        Send an update about a Property.
        :param property_: Property
        '''
        pass

    @abstractmethod
    def update_action(self, action: Action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        pass

    @abstractmethod
    def update_event(self, event: Event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        pass
