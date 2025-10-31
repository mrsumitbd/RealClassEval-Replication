
class Subscriber:
    """
    A class representing a subscriber that can be notified about updates to properties, actions, and events.
    """

    def __init__(self):
        """
        Initializes a new instance of the Subscriber class.
        """
        self.properties = {}
        self.actions = []
        self.events = []

    def update_property(self, property_):
        """
        Updates a property.

        Args:
            property_ (dict): A dictionary containing the property name and its new value.
        """
        if 'name' in property_ and 'value' in property_:
            self.properties[property_['name']] = property_['value']
        else:
            raise ValueError("Property update must contain 'name' and 'value'")

    def update_action(self, action):
        """
        Updates an action.

        Args:
            action (dict): A dictionary containing the action details.
        """
        if isinstance(action, dict):
            self.actions.append(action)
        else:
            raise ValueError("Action must be a dictionary")

    def update_event(self, event):
        """
        Updates an event.

        Args:
            event (dict): A dictionary containing the event details.
        """
        if isinstance(event, dict):
            self.events.append(event)
        else:
            raise ValueError("Event must be a dictionary")


# Example usage:
if __name__ == "__main__":
    subscriber = Subscriber()

    property_update = {'name': 'temperature', 'value': 25}
    subscriber.update_property(property_update)
    print(subscriber.properties)

    action = {'type': 'start', 'target': 'engine'}
    subscriber.update_action(action)
    print(subscriber.actions)

    event = {'type': 'alarm', 'message': 'System failure'}
    subscriber.update_event(event)
    print(subscriber.events)
