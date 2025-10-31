
class Subscriber:

    def __init__(self):
        self.properties = []
        self.actions = []
        self.events = []

    def update_property(self, property_):
        self.properties.append(property_)

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        self.actions.append(action)

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        self.events.append(event)
