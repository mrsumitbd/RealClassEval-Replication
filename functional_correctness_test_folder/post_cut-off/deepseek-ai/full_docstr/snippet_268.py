
class IndexManager:
    '''
    Automatically maintains in-memory indexes for fast lookup.
    '''

    def __init__(self):
        '''
        Initialize the IndexManager with empty indexes and document map.
        '''
        self._document_map = {}
        self._indexes = {}

    def index(self, doc):
        '''
        Index a document by adding it to the document map and updating the indexes.
        doc -- The document to index, should be a dictionary.
        '''
        doc_id = id(doc)
        self._document_map[doc_id] = doc
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
        doc_id = id(doc)
        if doc_id not in self._document_map:
            return
        del self._document_map[doc_id]
        for field, value in doc.items():
            if field in self._indexes and value in self._indexes[field]:
                self._indexes[field][value].discard(doc_id)
                if not self._indexes[field][value]:
                    del self._indexes[field][value]

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
        if field not in self._indexes or value not in self._indexes[field]:
            return []
        doc_ids = self._indexes[field][value]
        return [self._document_map[doc_id] for doc_id in doc_ids if doc_id in self._document_map]

    def query_in(self, field, values):
        '''
        Query the index for documents matching a specific field and a list of values.
        field -- The field to query.
        values -- The list of values to match in the field.
        Returns a list of documents that match the query.
        '''
        if field not in self._indexes:
            return []
        result = []
        for value in values:
            if value in self._indexes[field]:
                doc_ids = self._indexes[field][value]
                result.extend([self._document_map[doc_id]
                              for doc_id in doc_ids if doc_id in self._document_map])
        return result

    def clear(self):
        '''
        Clear all indexes and the document map.
        '''
        self._document_map.clear()
        self._indexes.clear()
