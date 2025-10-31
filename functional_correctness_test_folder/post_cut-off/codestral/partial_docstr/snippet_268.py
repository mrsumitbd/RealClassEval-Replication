
class IndexManager:

    def __init__(self):
        self.index = {}

    def index(self, doc):
        for field, value in doc.items():
            if field not in self.index:
                self.index[field] = {}
            if value not in self.index[field]:
                self.index[field][value] = []
            self.index[field][value].append(doc)

    def remove(self, doc):
        for field, value in doc.items():
            if field in self.index and value in self.index[field]:
                self.index[field][value].remove(doc)
                if not self.index[field][value]:
                    del self.index[field][value]

    def reindex(self, old_doc, new_doc):
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        if field in self.index and value in self.index[field]:
            return self.index[field][value]
        return []

    def query_in(self, field, values):
        results = []
        for value in values:
            results.extend(self.query(field, value))
        return results

    def clear(self):
        self.index = {}
