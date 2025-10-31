
class IndexManager:

    def __init__(self):
        self.indexes = {}

    def index(self, doc):
        for field, value in doc.items():
            if field not in self.indexes:
                self.indexes[field] = {}
            if value not in self.indexes[field]:
                self.indexes[field][value] = []
            self.indexes[field][value].append(doc)

    def remove(self, doc):
        for field, value in doc.items():
            if field in self.indexes and value in self.indexes[field]:
                if doc in self.indexes[field][value]:
                    self.indexes[field][value].remove(doc)
                    if not self.indexes[field][value]:
                        del self.indexes[field][value]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.indexes and value in self.indexes[field]:
            return self.indexes[field][value].copy()
        return []

    def query_in(self, field, values):
        result = []
        if field in self.indexes:
            for value in values:
                if value in self.indexes[field]:
                    result.extend(self.indexes[field][value])
        return result

    def clear(self):
        self.indexes.clear()
