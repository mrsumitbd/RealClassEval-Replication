
class IndexManager:

    def __init__(self):
        self.index_store = {}

    def index(self, doc):
        for field, value in doc.items():
            if field not in self.index_store:
                self.index_store[field] = {}
            if value not in self.index_store[field]:
                self.index_store[field][value] = set()
            self.index_store[field][value].add(doc)

    def remove(self, doc):
        for field, value in doc.items():
            if field in self.index_store and value in self.index_store[field]:
                self.index_store[field][value].discard(doc)
                if not self.index_store[field][value]:
                    del self.index_store[field][value]
                if not self.index_store[field]:
                    del self.index_store[field]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        return self.index_store.get(field, {}).get(value, set())

    def query_in(self, field, values):
        result = set()
        for value in values:
            result.update(self.index_store.get(field, {}).get(value, set()))
        return result

    def clear(self):
        self.index_store.clear()
