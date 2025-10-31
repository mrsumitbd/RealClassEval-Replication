
class Subscriber:

    def update_property(self, property_):
        # Implement logic to handle property update
        print(f"Property updated: {property_}")

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        # Implement logic to handle action update
        print(f"Action updated: {action}")

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
        # Implement logic to handle event update
        print(f"Event updated: {event}")
