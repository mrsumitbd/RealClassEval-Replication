
class IndexManager:

    def __init__(self):
        self.docs = set()
        self.indexes = {}

    def index(self, doc):
        doc_id = id(doc)
        if doc_id in self.docs:
            return
        self.docs.add(doc_id)
        for field, value in doc.items():
            if field not in self.indexes:
                self.indexes[field] = {}
            if value not in self.indexes[field]:
                self.indexes[field][value] = set()
            self.indexes[field][value].add(doc_id)
        # Store the doc itself for retrieval
        if not hasattr(self, '_doc_map'):
            self._doc_map = {}
        self._doc_map[doc_id] = doc

    def remove(self, doc):
        doc_id = id(doc)
        if doc_id not in self.docs:
            return
        for field, value in doc.items():
            if field in self.indexes and value in self.indexes[field]:
                self.indexes[field][value].discard(doc_id)
                if not self.indexes[field][value]:
                    del self.indexes[field][value]
                if not self.indexes[field]:
                    del self.indexes[field]
        self.docs.discard(doc_id)
        if hasattr(self, '_doc_map'):
            self._doc_map.pop(doc_id, None)

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.indexes and value in self.indexes[field]:
            doc_ids = self.indexes[field][value]
            return [self._doc_map[doc_id] for doc_id in doc_ids]
        return []

    def query_in(self, field, values):
        result_ids = set()
        if field in self.indexes:
            for value in values:
                if value in self.indexes[field]:
                    result_ids.update(self.indexes[field][value])
        return [self._doc_map[doc_id] for doc_id in result_ids]

    def clear(self):
        self.docs.clear()
        self.indexes.clear()
        if hasattr(self, '_doc_map'):
            self._doc_map.clear()
