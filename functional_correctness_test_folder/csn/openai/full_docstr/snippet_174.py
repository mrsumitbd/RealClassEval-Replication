class Subscriber:
    '''Abstract Subscriber class.'''

    def __init__(self):
        self.property_updates = []
        self.action_updates = []
        self.event_updates = []

    def update_property(self, property_):
        '''
        Send an update about a Property.
        :param property_: Property
        '''
        self.property_updates.append(property_)

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        self.action_updates.append(action)

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        self.event_updates.append(event)
