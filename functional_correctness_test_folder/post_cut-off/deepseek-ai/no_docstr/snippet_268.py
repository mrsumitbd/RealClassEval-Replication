
class IndexManager:

    def __init__(self):
        self._index = {}

    def index(self, doc):
        for field, value in doc.items():
            if field not in self._index:
                self._index[field] = {}
            if value not in self._index[field]:
                self._index[field][value] = set()
            self._index[field][value].add(doc)

    def remove(self, doc):
        for field, value in doc.items():
            if field in self._index and value in self._index[field]:
                self._index[field][value].discard(doc)
                if not self._index[field][value]:
                    del self._index[field][value]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self._index and value in self._index[field]:
            return self._index[field][value].copy()
        return set()

    def query_in(self, field, values):
        result = set()
        if field in self._index:
            for value in values:
                if value in self._index[field]:
                    result.update(self._index[field][value])
        return result

    def clear(self):
        self._index.clear()
