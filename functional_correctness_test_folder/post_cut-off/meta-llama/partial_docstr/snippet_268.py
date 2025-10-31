
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
            return [{'id': doc_id} for doc_id in self.index[field][value]]
        return []

    def query_in(self, field, values):
        result = set()
        if field in self.index:
            for value in values:
                if value in self.index[field]:
                    result.update(self.index[field][value])
        return [{'id': doc_id} for doc_id in result]

    def clear(self):
        self.index.clear()


# Example usage:
if __name__ == "__main__":
    index_manager = IndexManager()

    doc1 = {'id': 1, 'name': 'John', 'age': 25}
    doc2 = {'id': 2, 'name': 'Jane', 'age': 25}
    doc3 = {'id': 3, 'name': 'John', 'age': 30}

    index_manager.index(doc1)
    index_manager.index(doc2)
    index_manager.index(doc3)

    # Output: [{'id': 1}, {'id': 3}]
    print(index_manager.query('name', 'John'))
    print(index_manager.query('age', 25))  # Output: [{'id': 1}, {'id': 2}]
    # Output: [{'id': 1}, {'id': 2}, {'id': 3}]
    print(index_manager.query_in('name', ['John', 'Jane']))

    index_manager.remove(doc2)
    print(index_manager.query('age', 25))  # Output: [{'id': 1}]

    new_doc1 = {'id': 1, 'name': 'John', 'age': 26}
    index_manager.reindex(doc1, new_doc1)
    print(index_manager.query('age', 25))  # Output: []
    print(index_manager.query('age', 26))  # Output: [{'id': 1}]

    index_manager.clear()
    print(index_manager.query('name', 'John'))  # Output: []
