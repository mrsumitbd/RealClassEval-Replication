
class IndexManager:

    def __init__(self):
        self.indexes = {}

    def index(self, doc):
        for field, value in doc.items():
            if field not in self.indexes:
                self.indexes[field] = {}
            if value not in self.indexes[field]:
                self.indexes[field][value] = set()
            self.indexes[field][value].add(doc)

    def remove(self, doc):
        for field, value in doc.items():
            if field in self.indexes and value in self.indexes[field]:
                self.indexes[field][value].discard(doc)

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.indexes and value in self.indexes[field]:
            return self.indexes[field][value]
        return set()

    def query_in(self, field, values):
        result = set()
        if field in self.indexes:
            for value in values:
                if value in self.indexes[field]:
                    result.update(self.indexes[field][value])
        return result

    def clear(self):
        self.indexes = {}
