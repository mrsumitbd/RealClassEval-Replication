class KnowledgeBase:

    def __init__(self):
        self.__dict__['entries'] = {}

    def __contains__(self, key):
        return key in self.entries

    def __setattr__(self, key, value):
        if key not in self:
            self.entries[key] = value
        else:
            raise AttributeError(key)

    def __getattr__(self, key):
        if key in self:
            return self.entries[key]
        else:
            raise AttributeError(key)