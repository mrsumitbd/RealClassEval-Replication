
class Subscriber:

    def update_property(self, property_):
        print(f"Received update about Property: {property_}")

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        print(f"Received update about Action: {action}")

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        print(f"Received update about Event: {event}")
