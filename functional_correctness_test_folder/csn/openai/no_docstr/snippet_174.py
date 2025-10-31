
class Subscriber:
    def __init__(self):
        self._properties = []
        self._actions = []
        self._events = []

    def update_property(self, property_):
        """Record a property update."""
        self._properties.append(property_)

    def update_action(self, action):
        """Record an action update."""
        self._actions.append(action)

    def update_event(self, event):
        """Record an event update."""
        self._events.append(event)

    @property
    def properties(self):
        return list(self._properties)

    @property
    def actions(self):
        return list(self._actions)

    @property
    def events(self):
        return list(self._events)

    def __repr__(self):
        return (
            f"<Subscriber properties={self._properties} "
            f"actions={self._actions} events={self._events}>"
        )
