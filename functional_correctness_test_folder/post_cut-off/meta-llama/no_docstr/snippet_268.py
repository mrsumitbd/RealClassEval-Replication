
class IndexManager:

    def __init__(self):
        self.index = {}

    def index(self, doc):
        doc_id = doc['id']
        for field, value in doc.items():
            if field != 'id':
                if field not in self.index:
                    self.index[field] = {}
                if value not in self.index[field]:
                    self.index[field][value] = set()
                self.index[field][value].add(doc_id)

    def remove(self, doc):
        doc_id = doc['id']
        for field, value in doc.items():
            if field != 'id' and field in self.index and value in self.index[field]:
                self.index[field][value].discard(doc_id)
                if not self.index[field][value]:
                    del self.index[field][value]
                if not self.index[field]:
                    del self.index[field]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.index and value in self.index[field]:
            return list(self.index[field][value])
        return []

    def query_in(self, field, values):
        result = set()
        if field in self.index:
            for value in values:
                if value in self.index[field]:
                    result.update(self.index[field][value])
        return list(result)

    def clear(self):
        self.index.clear()
