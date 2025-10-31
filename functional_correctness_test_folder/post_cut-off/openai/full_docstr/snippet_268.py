
class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._docs = {}          # doc_id -> doc
        self._indexes = {}       # field -> {value -> set(doc_id)}

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError("Document must be a dictionary")
        doc_id = id(doc)
        if doc_id in self._docs:
            # Already indexed; ignore or update? We'll ignore duplicates.
            return
        self._docs[doc_id] = doc
        for field, value in doc.items():
            if field not in self._indexes:
                self._indexes[field] = {}
            if value not in self._indexes[field]:
                self._indexes[field][value] = set()
            self._indexes[field][value].add(doc_id)

    def remove(self, doc):
        '''
        Remove a document from the index.
        doc -- The document to remove, should be a dictionary.
        '''
        if not isinstance(doc, dict):
            raise TypeError("Document must be a dictionary")
        doc_id = id(doc)
        if doc_id not in self._docs:
            return
        # Remove from indexes
        for field, value in doc.items():
            field_index = self._indexes.get(field)
            if field_index is None:
                continue
            doc_set = field_index.get(value)
            if doc_set is None:
                continue
            doc_set.discard(doc_id)
            if not doc_set:
                del field_index[value]
            if not field_index:
                del self._indexes[field]
        # Remove from docs
        del self._docs[doc_id]

    def reindex(self, old_doc, new_doc):
        '''
        Reindex a document by removing the old document and adding the new one.
        old_doc -- The document to remove from the index.
        new_doc -- The document to add to the index.
        '''
        self.remove(old_doc)
        self.index(new_doc)

    def query(self, field, value):
        '''
        Query the index for documents matching a specific field and value.
        field -- The field to query.
        value -- The value to match in the field.
        Returns a list of documents that match the query.
        '''
        field_index = self._indexes.get(field)
        if not field_index:
            return []
        doc_ids = field_index.get(value, set())
        return [self._docs[doc_id] for doc_id in doc_ids]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        if not isinstance(values, (list, set, tuple)):
            raise TypeError("values must be a list, set, or tuple")
        field_index = self._indexes.get(field)
        if not field_index:
            return []
        result_ids = set()
        for value in values:
            ids = field_index.get(value)
            if ids:
                result_ids.update(ids)
        return [self._docs[doc_id] for doc_id in result_ids]

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._docs.clear()
        self._indexes.clear()
