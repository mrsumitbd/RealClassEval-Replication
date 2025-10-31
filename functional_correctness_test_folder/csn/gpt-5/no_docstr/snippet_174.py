class Subscriber:
    def __init__(self):
        self.properties = []
        self.actions = []
        self.events = []
        self._counts = {"property": 0, "action": 0, "event": 0}

    def update_property(self, property_):
        self.properties.append(property_)
        self._counts["property"] += 1
        return property_

    def update_action(self, action):
        self.actions.append(action)
        self._counts["action"] += 1
        return action

    def update_event(self, event):
        self.events.append(event)
        self._counts["event"] += 1
        return event
