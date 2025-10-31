
class IndexManager:

    def __init__(self):
        self.index_store = {}

    def index(self, doc):
        doc_id = doc.get('id')
        if doc_id is not None:
            for key, value in doc.items():
                if key != 'id':
                    if key not in self.index_store:
                        self.index_store[key] = {}
                    if value not in self.index_store[key]:
                        self.index_store[key][value] = set()
                    self.index_store[key][value].add(doc_id)

    def remove(self, doc):
        doc_id = doc.get('id')
        if doc_id is not None:
            for key, value in doc.items():
                if key != 'id' and key in self.index_store and value in self.index_store[key]:
                    self.index_store[key][value].discard(doc_id)
                    if not self.index_store[key][value]:
                        del self.index_store[key][value]
                    if not self.index_store[key]:
                        del self.index_store[key]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.index_store and value in self.index_store[field]:
            return [doc_id for doc_id in self.index_store[field][value]]
        return []

    def query_in(self, field, values):
        if field in self.index_store:
            result = set()
            for value in values:
                if value in self.index_store[field]:
                    result.update(self.index_store[field][value])
            return list(result)
        return []

    def clear(self):
        self.index_store.clear()
