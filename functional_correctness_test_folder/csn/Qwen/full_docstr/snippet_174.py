
class Subscriber:
    '''Abstract Subscriber class.'''

    def update_property(self, property_):
        '''
        Send an update about a Property.
        :param property_: Property
        '''
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        raise NotImplementedError(
            "This method should be overridden by subclasses")
