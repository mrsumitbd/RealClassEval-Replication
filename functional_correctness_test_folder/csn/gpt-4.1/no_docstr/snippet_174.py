
class Subscriber:

    def __init__(self):
        self.properties = []
        self.actions = []
        self.events = []

    def update_property(self, property_):
        self.properties.append(property_)

    def update_action(self, action):
        self.actions.append(action)

    def update_event(self, event):
        self.events.append(event)
