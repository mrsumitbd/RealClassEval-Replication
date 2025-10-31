
class Subscriber:
    def __init__(self):
        # Store all updates received by this subscriber
        self.updates = []

    def update_property(self, property_):
        """
        Receive an update about a property change.
        :param property_: Any object representing the property.
        """
        self.updates.append(('property', property_))

    def update_action(self, action):
        """
        Send an update about an Action.
        :param action: Action
        """
        self.updates.append(('action', action))

    def update_event(self, event):
        """
        Send an update about an Event.
        :param event: Event
        """
        self.updates.append(('event', event))
