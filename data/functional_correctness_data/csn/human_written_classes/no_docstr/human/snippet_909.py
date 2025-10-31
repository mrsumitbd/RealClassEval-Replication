class EventManager:

    def __init__(self):
        self.functions = []

    def register(self, callback, trigger):
        self.functions.append((callback, trigger))

    def unregister(self, callback, trigger):
        for c, t in self.functions:
            if c == callback and (trigger is None or t == trigger):
                self.functions.remove((c, t))

    def trigger(self, data):
        for callback, trigger in self.functions:
            if trigger is None or isinstance(data, trigger):
                callback(data)