
class Cache:

    def __init__(self):
        self.storage = {}

    def clear(self):
        self.storage.clear()

    def get(self, key, creator):
        if key not in self.storage:
            self.storage[key] = creator()
        return self.storage[key]
