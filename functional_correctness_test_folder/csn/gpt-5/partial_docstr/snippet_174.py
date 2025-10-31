class Subscriber:
    def __init__(self):
        self._properties = []
        self._actions = []
        self._events = []

    def update_property(self, property_):
        self._properties.append(property_)

    def update_action(self, action):
        '''
        Send an update about an Action.
        :param action: Action
        '''
        self._actions.append(action)

    def update_event(self, event):
        '''
        Send an update about an Event.
        :param event: Event
        '''
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

    def last_property(self):
        return self._properties[-1] if self._properties else None

    def last_action(self):
        return self._actions[-1] if self._actions else None

    def last_event(self):
        return self._events[-1] if self._events else None
